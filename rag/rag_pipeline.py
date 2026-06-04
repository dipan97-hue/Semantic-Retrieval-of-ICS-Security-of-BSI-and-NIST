from embeddings.embedding_model import emb_query
from retrieval.retrieve import retrieve
from retrieval.mappings import get_full_mappings
from retrieval.context_building import build_context
from prompts.prompt_builder import build_prompt
from llm.llm_router import generate_answer
from llm.llm_judge import evaluate_complete_rag

import warnings

warnings.filterwarnings("ignore")


def enrich_results(results):

    clean_results = []

    for r in results:

        if not isinstance(r, dict) or "chunk_id" not in r:
            continue

        try:
            r["mappings"] = get_full_mappings(r["chunk_id"])

        except Exception:
            r["mappings"] = []

        clean_results.append(r)

    return clean_results


def generate_context(query, results):

    context = build_context(results)

    prompt = build_prompt(
        query=query,
        context=context
    )

    return context, prompt


def generate_llm_answer(model_name, prompt):

    try:

        return generate_answer(
            model_name=model_name,
            prompt=prompt
        )

    except Exception as e:

        print("LLM ERROR:", e)

        return "Answer generation failed."


def evaluate_response(query, context, answer, results, model_name):

    try:

        return evaluate_complete_rag(
            query=query,
            retrieved_context=context,
            generated_answer=answer,
            results=results,
            model_name=model_name
        )

    except Exception as e:

        print("JUDGE ERROR:", e)

        return "Evaluation failed."


def rag(query, model_name, k=10):

    if not query or not query.strip():

        return {
            "query": query,
            "answer": "Please enter a query.",
            "results": [],
            "context": "",
            "evaluation_output": ""
        }

    query_embedding = emb_query(query)

    results = retrieve(
        query_embedding,
        k
    )

    print("RETRIEVAL RESULTS:")
    print(results)

    if not isinstance(results, list) or len(results) == 0:

        return {
            "query": query,
            "answer": "No relevant requirements were found.",
            "results": [],
            "context": "",
            "evaluation_output": ""
        }

    top_score = results[0].get(
        "similarity",
        0
    )

    if top_score < 0.40:

        return {
            "query": query,
            "answer":
                """
No relevant OT cybersecurity requirements were found.

Please ask questions related to:

• PLC Security
• Authentication
• Backup & Recovery
• ICS / SCADA
• Network Segmentation
• Monitoring
• OT Security Controls
• Governance
• BSI IT-Grundschutz
• NIST SP 800-82
                """,
            "results": [],
            "context": "",
            "evaluation_output": ""
        }

    clean_results = enrich_results(results)

    context, prompt = generate_context(
        query,
        clean_results
    )

    answer = generate_llm_answer(
        model_name,
        prompt
    )

    evaluation_output = evaluate_response(
        query=query,
        context=context,
        answer=answer,
        results=clean_results,
        model_name=model_name
    )

    return {
        "query": query,
        "answer": answer,
        "results": clean_results,
        "context": context,
        "evaluation_output": evaluation_output
    }