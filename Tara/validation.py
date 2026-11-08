import json
import re

from llm.llm_router import generate_answer

from rag.rag_pipeline import rag

from Tara.prompts import build_tara_prompt

from Tara.model import (
    CYBERSECURITY_PROPERTIES,
    IMPACT_CATEGORIES,
    IMPACT_RATINGS,
    THREAT_TYPES,
    RISK_TREATMENTS
)

from Tara.scoring import (
    ELAPSED_TIME,
    SPECIALIST_EXPERTISE,
    KNOWLEDGE,
    WINDOW_OF_OPPORTUNITY,
    EQUIPMENT,
    calculate_attack_potential
)


def validate_asset(asset):
    errors = []

    if not asset.get("id"):
        errors.append("Asset ID is required.")

    if not asset.get("name"):
        errors.append("Asset name is required.")

    properties = asset.get("cybersecurity_properties", [])

    if not properties:
        errors.append("At least one cybersecurity property is required.")

    for prop in properties:
        if prop not in CYBERSECURITY_PROPERTIES:
            errors.append(f"Invalid cybersecurity property: {prop}")

    return errors


def validate_damage_scenario(damage):
    errors = []

    if damage.get("impact_category") not in IMPACT_CATEGORIES:
        errors.append("Invalid impact category.")

    if damage.get("impact_rating") not in IMPACT_RATINGS:
        errors.append("Invalid impact rating.")

    if not damage.get("asset_id"):
        errors.append("Damage scenario must reference an asset.")

    return errors


def validate_threat_scenario(threat):
    errors = []

    if threat.get("threat_type") not in THREAT_TYPES:
        errors.append("Invalid STRIDE threat type.")

    if not threat.get("asset_id"):
        errors.append("Threat scenario must reference an asset.")

    if not threat.get("damage_scenario_id"):
        errors.append("Threat scenario must reference a damage scenario.")

    return errors


def validate_attack_path_step(step):
    errors = []

    factor_fields = {
        "elapsed_time": ELAPSED_TIME,
        "specialist_expertise": SPECIALIST_EXPERTISE,
        "knowledge_of_item": KNOWLEDGE,
        "window_of_opportunity": WINDOW_OF_OPPORTUNITY,
        "equipment": EQUIPMENT
    }

    for field, allowed_values in factor_fields.items():

        value = step.get(field)

        if value is None or value == "":
            errors.append(f"Missing attack-potential factor: {field}")

        elif value not in allowed_values:
            errors.append(f"Invalid {field}: {value}")

    if not step.get("description"):
        errors.append("Attack-path step description is required.")

    return errors


def validate_treatment(treatment, rationale=None):
    errors = []

    if treatment not in RISK_TREATMENTS:
        errors.append("Invalid risk treatment.")

    if treatment in ["Share", "Retain"] and not (
        rationale and rationale.strip()
    ):
        errors.append(
            "A rationale is required for Share or Retain."
        )

    return errors


def validate_attack_path(steps):
    errors = []

    if not steps:
        return ["Attack path must contain at least one step."]

    for index, step in enumerate(steps, start=1):
        step_errors = validate_attack_path_step(step)

        for error in step_errors:
            errors.append(f"Step {index}: {error}")

    return errors


def validate_attack_potential(step):
    """Calculate APS only after validating all five factors."""

    errors = validate_attack_path_step(step)

    if errors:
        return None, errors

    return calculate_attack_potential(step), []
