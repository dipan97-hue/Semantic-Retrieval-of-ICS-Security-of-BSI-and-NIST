import json
import os
import warnings
from rag.rag_pipeline import rag
from llm.crossmodel_judge import (
    generate_all_configurations,
    cross_model_judge,
    aggregate_results,
    calculate_top_k_ranking
)

warnings.filterwarnings("ignore")
QUERIES = [
    "What security measures should be implemented to protect PLCs in an industrial control system?"
]


OUTPUT_FILE = "results/cross_model_results.json"


def run_experiment():

    all_results = []

    for i, query in enumerate(QUERIES, start=1):

        print("\n" + "=" * 60)
        print(f"QUERY {i}/{len(QUERIES)}")
        print(query)
        print("=" * 60)

        # 1. Generate 12 answers
        generated_results = generate_all_configurations(
            query=query,
            rag_function=rag
        )

        # 2. Cross-model judging
        evaluations = cross_model_judge(
            query=query,
            generated_results=generated_results
        )

        result = {
            "query_id": f"Q{i:02d}",
            "query": query,
            "evaluations": evaluations
        }

        all_results.append(result)

        # Save after every query
        os.makedirs("results", exist_ok=True)

        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                all_results,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(f"Saved Q{i:02d}")

    print("\nExperiment completed.")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    run_experiment()