import json
import re

from llm.llm_router import generate_answer
from prompts.judge_prompts import build_cross_model_judge_prompt


# ============================================================
# MODELS
# ============================================================

MODELS = [
    "gpt-5.4-nano",
    "gemini-3.1-flash-lite",
    "claude-haiku-4-5"
]


# ============================================================
# TOP-K VALUES
# ============================================================

TOP_K_VALUES = [10, 20, 30]


# ============================================================
# GENERATE ALL MODEL + K CONFIGURATIONS
# ============================================================

def generate_all_configurations(query, rag_function):

    generated_results = {}

    for model in MODELS:

        generated_results[model] = {}

        for k in TOP_K_VALUES:

            print(
                f"\nGenerating answer | "
                f"Model={model} | K={k}"
            )

            try:

                result = rag_function(
                    query=query,
                    model_name=model,
                    k=k,
                    run_judge=False
                )

                generated_results[model][k] = result

            except Exception as e:

                print(
                    f"Generation failed | "
                    f"Model={model} | K={k}"
                )

                generated_results[model][k] = {
                    "query": query,
                    "answer": "Generation failed.",
                    "results": [],
                    "context": "",
                    "evaluation_output": "",
                    "model_name": model,
                    "top_k": k,
                    "error": str(e)
                }

    return generated_results


# ============================================================
# EXTRACT JSON FROM JUDGE RESPONSE
# ============================================================

def extract_json(response):

    if isinstance(response, dict):
        return response

    text = str(response).strip()

    # Try direct JSON
    try:

        return json.loads(text)

    except Exception:
        pass

    # Try extracting JSON from surrounding text
    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if match:

        try:

            return json.loads(
                match.group()
            )

        except Exception:
            pass

    return {
        "error": "Unable to parse judge response",
        "raw_response": text
    }


# ============================================================
# CALCULATE WEIGHTED SCORE
# ============================================================

def calculate_score(evaluation):

    if "error" in evaluation:
        return None

    criteria = [
        "relevance",
        "technical_accuracy",
        "faithfulness",
        "completeness",
        "ot_operational_suitability",
        "bsi_nist_alignment",
        "hallucination_risk",
        "overall_quality"
    ]

    scores = []

    for criterion in criteria:

        value = evaluation.get(criterion)

        if value is None:
            return None

        scores.append(float(value))

    return round(sum(scores) / len(scores),3)


# ============================================================
# JUDGE ONE CANDIDATE
# ============================================================

def judge_candidate(
    judge_model,
    query,
    candidate_model,
    candidate_k,
    candidate_result
):

    candidate_answer = candidate_result.get(
        "answer",
        ""
    )

    candidate_context = candidate_result.get(
        "context",
        ""
    )

    # Build blind evaluation prompt.
    #
    # IMPORTANT:
    # candidate_model and candidate_k are NOT
    # included in the prompt.
    #
    # This prevents the judge from knowing
    # which model generated the answer.

    prompt = build_cross_model_judge_prompt(

        query=query,

        candidate_answer=candidate_answer,

        candidate_context=candidate_context

    )

    try:

        print(
            f"Judging | "
            f"Judge={judge_model} | "
            f"Candidate={candidate_model} | "
            f"K={candidate_k}"
        )

        response = generate_answer(

            model_name=judge_model,

            prompt=prompt

        )

        evaluation = extract_json(
            response
        )

        # Store metadata outside the prompt.
        evaluation["judge_model"] = judge_model

        evaluation["candidate_model"] = (
            candidate_model
        )

        evaluation["top_k"] = candidate_k

        # Calculate score in Python.
        evaluation["score"] = calculate_score(
            evaluation
        )

        return evaluation

    except Exception as e:

        print(
            f"Judge failed | "
            f"Judge={judge_model} | "
            f"Candidate={candidate_model} | "
            f"K={candidate_k}"
        )

        return {

            "judge_model": judge_model,

            "candidate_model": candidate_model,

            "top_k": candidate_k,

            "score": None,

            "error": str(e)

        }


# ============================================================
# CROSS-MODEL JUDGING
# ============================================================

def cross_model_judge(
    query,
    generated_results
):

    evaluations = []

    # Candidate model
    for candidate_model in MODELS:

        # Candidate Top-K
        for k in TOP_K_VALUES:

            candidate_result = (
                generated_results
                .get(candidate_model, {})
                .get(k)
            )

            if not candidate_result:
                continue

            # Every other model becomes a judge
            for judge_model in MODELS:

                # NEVER allow self-judging
                if judge_model == candidate_model:
                    continue

                evaluation = judge_candidate(

                    judge_model=judge_model,

                    query=query,

                    candidate_model=candidate_model,

                    candidate_k=k,

                    candidate_result=candidate_result

                )

                evaluations.append(
                    evaluation
                )

    return evaluations


# ============================================================
# AGGREGATE MODEL + TOP-K SCORES
# ============================================================

def aggregate_results(evaluations):

    grouped = {}

    for evaluation in evaluations:

        candidate_model = evaluation.get(
            "candidate_model"
        )

        k = evaluation.get(
            "top_k"
        )

        score = evaluation.get(
            "score"
        )

        if (
            candidate_model is None
            or k is None
            or score is None
        ):
            continue

        key = (
            candidate_model,
            k
        )

        if key not in grouped:

            grouped[key] = []

        grouped[key].append(
            score
        )

    ranking = []

    for (
        model,
        k
    ), scores in grouped.items():

        average_score = (
            sum(scores)
            / len(scores)
        )

        ranking.append({

            "model": model,

            "top_k": k,

            "average_score": round(
                average_score,
                3
            ),

            "judge_count": len(
                scores
            )

        })

    # Highest score first
    ranking.sort(

        key=lambda x:
        x["average_score"],

        reverse=True

    )

    return ranking


# ============================================================
# CALCULATE TOP-K RANKING
# ============================================================

def calculate_top_k_ranking(ranking):

    grouped = {}

    for item in ranking:

        k = item["top_k"]

        score = item[
            "average_score"
        ]

        if k not in grouped:

            grouped[k] = []

        grouped[k].append(
            score
        )

    results = []

    for k, scores in grouped.items():

        average_score = (
            sum(scores)
            / len(scores)
        )

        results.append({

            "top_k": k,

            "average_score": round(
                average_score,
                3
            )

        })

    results.sort(

        key=lambda x:
        x["average_score"],

        reverse=True

    )

    return results