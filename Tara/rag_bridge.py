
from rag.rag_pipeline import rag


def retrieve_security_evidence(requirements, model_name, k=10):
    """
    Retrieve NIST and BSI evidence for each TARA-generated
    cybersecurity requirement using the existing RAG pipeline.
    """

    evidence = []

    for requirement in requirements:

        result = rag(
            query=requirement,
            model_name=model_name,
            k=k,
            run_judge=False
        )

        evidence.append({
            "requirement": requirement,
            "answer": result.get("answer"),
            "results": result.get("results", []),
            "context": result.get("context", "")
        })

    return evidence
