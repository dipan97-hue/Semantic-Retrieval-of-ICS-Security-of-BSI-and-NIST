
import json
import re

from rag.rag_pipeline import rag
from llm.llm_router import generate_answer

from Tara.prompts import build_tara_prompt
from Tara.scoring import assess_attack_path, calculate_risk
from Tara.validation import (
    validate_asset,
    validate_damage_scenario,
    validate_threat_scenario,
    validate_attack_path,
    validate_treatment,
)
from Tara.rag_bridge import retrieve_security_evidence


# ============================================================
# 1. PARSE LLM JSON
# ============================================================

def parse_llm_json(response):
    """Parse JSON returned by an LLM."""

    if isinstance(response, dict):
        return response

    if not isinstance(response, str):
        raise ValueError("LLM returned an invalid response.")

    cleaned = response.strip()

    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()

        for index, char in enumerate(cleaned):
            if char == "{":
                try:
                    result, _ = decoder.raw_decode(cleaned[index:])
                    if isinstance(result, dict):
                        return result
                except json.JSONDecodeError:
                    continue

    raise ValueError("No valid JSON object found in LLM response.")


# ============================================================
# 2. QUERY CLASSIFICATION
# ============================================================

def classify_query(query, model_name):
    """Classify a query as RAG or TARA."""

    classification_prompt = f"""
You are an OT cybersecurity query classifier.

Choose TARA when the user describes a specific industrial
system, asset, vulnerability, threat, attack path, or
system-specific risk assessment.

Choose RAG for general OT cybersecurity explanations,
standards, security controls, and recommendations.

Examples:
- Our PLC uses shared passwords. Assess the risk. -> TARA
- An attacker could modify our SCADA configuration. -> TARA
- Explain network segmentation in OT. -> RAG
- What does NIST SP 800-82 recommend? -> RAG

USER QUERY:
{query}

Return JSON only:
{{
    "route": "TARA",
    "reason": "Short explanation"
}}
"""

    response = generate_answer(
        model_name,
        classification_prompt
    )

    result = parse_llm_json(response)

    route = str(result.get("route", "RAG")).upper().strip()

    if route not in ("TARA", "RAG"):
        raise ValueError(f"Invalid classifier route: {route}")

    return {
        "route": route,
        "reason": result.get("reason", "")
    }


# ============================================================
# 3. VALIDATE TARA STRUCTURE
# ============================================================

def validate_tara_structure(data):
    """Validate TARA entities and their relationships."""

    errors = []

    if not isinstance(data, dict):
        return ["TARA response must be a JSON object."]

    item = data.get("item")

    if not isinstance(item, dict):
        errors.append("Missing or invalid item definition.")
        return errors

    for field in ("id", "name", "description"):
        if not item.get(field):
            errors.append(f"Item is missing required field: {field}")

    assets = data.get("assets", [])
    damages = data.get("damage_scenarios", [])
    threats = data.get("threat_scenarios", [])
    attack_paths = data.get("attack_paths", [])

    if not isinstance(assets, list):
        return errors + ["Assets must be a list."]

    if not isinstance(damages, list):
        return errors + ["Damage scenarios must be a list."]

    if not isinstance(threats, list):
        return errors + ["Threat scenarios must be a list."]

    if not isinstance(attack_paths, list):
        return errors + ["Attack paths must be a list."]

    asset_ids = {
        asset.get("id")
        for asset in assets
        if isinstance(asset, dict)
    }

    damage_ids = {
        damage.get("id")
        for damage in damages
        if isinstance(damage, dict)
    }

    threat_ids = {
        threat.get("id")
        for threat in threats
        if isinstance(threat, dict)
    }

    for asset in assets:
        if not isinstance(asset, dict):
            errors.append("Invalid asset object.")
            continue

        try:
            validate_asset(asset)
        except Exception as exc:
            errors.append(f"Asset validation: {exc}")

    for damage in damages:
        if not isinstance(damage, dict):
            errors.append("Invalid damage scenario object.")
            continue

        if damage.get("asset_id") not in asset_ids:
            errors.append(
                f"Damage scenario {damage.get('id')} references an unknown asset."
            )

        try:
            validate_damage_scenario(damage)
        except Exception as exc:
            errors.append(f"Damage scenario validation: {exc}")

    for threat in threats:
        if not isinstance(threat, dict):
            errors.append("Invalid threat scenario object.")
            continue

        if threat.get("asset_id") not in asset_ids:
            errors.append(
                f"Threat scenario {threat.get('id')} references an unknown asset."
            )

        if threat.get("damage_scenario_id") not in damage_ids:
            errors.append(
                f"Threat scenario {threat.get('id')} references an unknown damage scenario."
            )

        try:
            validate_threat_scenario(threat)
        except Exception as exc:
            errors.append(f"Threat scenario validation: {exc}")

    for path in attack_paths:
        if not isinstance(path, dict):
            errors.append("Invalid attack path object.")
            continue

        if path.get("threat_scenario_id") not in threat_ids:
            errors.append(
                f"Attack path {path.get('id')} references an unknown threat scenario."
            )

        try:
            validate_attack_path(path.get("steps", []))
        except Exception as exc:
            errors.append(f"Attack path validation: {exc}")

    return errors


# ============================================================
# 4. CALCULATE TARA RISKS
# ============================================================
def calculate_tara_risks(data):
    """Calculate attack feasibility and risk for each attack path."""

    results = []

    threats = {
        threat["id"]: threat
        for threat in data.get("threat_scenarios", [])
    }

    damages = {
        damage["id"]: damage
        for damage in data.get("damage_scenarios", [])
    }

    for path in data.get("attack_paths", []):

        threat = threats.get(path.get("threat_scenario_id"))

        if not threat:
            continue

        damage = damages.get(threat.get("damage_scenario_id"))

        if not damage:
            continue

        # Calculate attack path result
        attack_path_result = assess_attack_path(
            path.get("steps", [])
        )

        # Calculate risk
        risk_value = calculate_risk(
            damage["impact_rating"],
            attack_path_result["attack_feasibility_rating"]
        )

        results.append({
            "attack_path_id": path.get("id"),
            "threat_scenario_id": threat.get("id"),
            "damage_scenario_id": damage.get("id"),

            "impact_category": damage.get("impact_category"),
            "impact_rating": damage.get("impact_rating"),

            # Nested structure expected by app.py
            "attack_path_result": attack_path_result,

            "risk_value": risk_value
        })

    return results
# ============================================================
# 5. RUN TARA ANALYSIS
# ============================================================

def run_tara_analysis(user_problem, model_name, k=10):
    """Generate, validate, score and enrich TARA analysis."""

    prompt = build_tara_prompt(user_problem)

    response = generate_answer(
        model_name,
        prompt
    )

    tara_data = parse_llm_json(response)

    validation_errors = validate_tara_structure(tara_data)

    if validation_errors:
        return {
            "analysis_status": "Validation failed",
            "tara_data": tara_data,
            "validation_errors": validation_errors,
            "risk_results": [],
            "evidence": []
        }

    risk_results = calculate_tara_risks(tara_data)

    requirements = tara_data.get(
        "cybersecurity_requirements",
        []
    )

    evidence = []

    if requirements:
        evidence = retrieve_security_evidence(
            requirements=requirements,
            model_name=model_name,
            k=k
        )

    return {
        "analysis_status": "Completed",
        "tara_data": tara_data,
        "validation_errors": [],
        "risk_results": risk_results,
        "evidence": evidence
    }


# ============================================================
# 6. MAIN ANALYSIS
# ============================================================

def analyze_query(query, model_name, k=10):
    """
    Always run original RAG first.
    Add TARA only when classification identifies a
    system-specific cybersecurity problem.
    """

    # Original RAG remains unchanged.
    rag_result = rag(
        query=query,
        model_name=model_name,
        k=k,
        run_judge=False
    )

    # Classification
    try:
        classification = classify_query(
            query=query,
            model_name=model_name
        )
    except Exception as exc:
        return {
            "mode": "RAG",
            "classification": {
                "route": "UNKNOWN",
                "reason": f"Classification failed: {exc}"
            },
            "classification_error": str(exc),
            "rag_result": rag_result,
            "tara_result": None
        }

    # General RAG question
    if classification["route"] == "RAG":
        return {
            "mode": "RAG",
            "classification": classification,
            "rag_result": rag_result,
            "tara_result": None
        }

    # Additional TARA analysis
    try:
        tara_result = run_tara_analysis(
            user_problem=query,
            model_name=model_name,
            k=k
        )

        tara_result["classification"] = classification

    except Exception as exc:
        tara_result = {
            "analysis_status": "Failed",
            "error": str(exc),
            "classification": classification
        }

    return {
        "mode": "TARA",
        "classification": classification,
        "rag_result": rag_result,
        "tara_result": tara_result
    }
