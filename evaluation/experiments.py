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


# ============================================================
# EXPERIMENT QUERIES
# ============================================================

QUERIES = [

    # --------------------------------------------------------
    # PLC Security
    # --------------------------------------------------------

    {
        "query_id": "Q01",
        "category": "PLC Security",
        "query": "How should PLCs be authenticated in OT environments?"
    },

    {
        "query_id": "Q02",
        "category": "PLC Security",
        "query": "What security controls should be applied to PLC programming interfaces?"
    },


    # --------------------------------------------------------
    # Authentication
    # --------------------------------------------------------

    {
        "query_id": "Q03",
        "category": "Authentication",
        "query": "How should user authentication be implemented in ICS systems?"
    },

    {
        "query_id": "Q04",
        "category": "Authentication",
        "query": "What authentication mechanisms are recommended for OT environments?"
    },


    # --------------------------------------------------------
    # Backup & Recovery
    # --------------------------------------------------------

    {
        "query_id": "Q05",
        "category": "Backup & Recovery",
        "query": "How should OT backups be protected?"
    },

    {
        "query_id": "Q06",
        "category": "Backup & Recovery",
        "query": "What recovery procedures should be established for industrial systems?"
    },


    # --------------------------------------------------------
    # ICS / SCADA
    # --------------------------------------------------------

    {
        "query_id": "Q07",
        "category": "ICS / SCADA",
        "query": "What security requirements apply to SCADA systems?"
    },

    {
        "query_id": "Q08",
        "category": "ICS / SCADA",
        "query": "How should ICS assets be identified and managed?"
    },


    # --------------------------------------------------------
    # Network Segmentation
    # --------------------------------------------------------

    {
        "query_id": "Q09",
        "category": "Network Segmentation",
        "query": "How should OT networks be segmented?"
    },

    {
        "query_id": "Q10",
        "category": "Network Segmentation",
        "query": "What is the role of security zones and conduits?"
    },


    # --------------------------------------------------------
    # Monitoring
    # --------------------------------------------------------

    {
        "query_id": "Q11",
        "category": "Monitoring",
        "query": "How should security monitoring be implemented in OT?"
    },

    {
        "query_id": "Q12",
        "category": "Monitoring",
        "query": "What events should be logged in ICS environments?"
    },


    # --------------------------------------------------------
    # OT Security Controls
    # --------------------------------------------------------

    {
        "query_id": "Q13",
        "category": "OT Security Controls",
        "query": "What security controls protect industrial systems?"
    },

    {
        "query_id": "Q14",
        "category": "OT Security Controls",
        "query": "How should vulnerability management be performed in OT?"
    },


    # --------------------------------------------------------
    # Governance
    # --------------------------------------------------------

    {
        "query_id": "Q15",
        "category": "Governance",
        "query": "How should OT cybersecurity governance be established?"
    },

    {
        "query_id": "Q16",
        "category": "Governance",
        "query": "What responsibilities should OT security roles have?"
    }
]


# ============================================================
# OUTPUT FILE
# ============================================================

OUTPUT_FILE = "results/cross_model_results.json"


# ============================================================
# RUN EXPERIMENT
# ============================================================

def run_experiment():

    all_results = []

    for item in QUERIES:

        query_id = item["query_id"]
        category = item["category"]
        query = item["query"]

        print("\n" + "=" * 60)
        print(
            f"{query_id} | "
            f"{category}"
        )
        print(query)
        print("=" * 60)


        # ====================================================
        # 1. GENERATE 12 ANSWERS
        # ====================================================

        generated_results = generate_all_configurations(
            query=query,
            rag_function=rag
        )


        # ====================================================
        # 2. CROSS-MODEL JUDGING
        # ====================================================

        evaluations = cross_model_judge(
            query=query,
            generated_results=generated_results
        )


        # ====================================================
        # 3. STORE ONLY EVALUATIONS
        # ====================================================

        result = {

            "query_id": query_id,

            "category": category,

            "query": query,

            "evaluations": evaluations

        }

        all_results.append(result)


        # ====================================================
        # 4. SAVE AFTER EVERY QUERY
        # ====================================================

        os.makedirs(
            "results",
            exist_ok=True
        )

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


        print(
            f"Saved {query_id}"
        )


    print("\nExperiment completed.")

    print(
        f"Results saved to: {OUTPUT_FILE}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run_experiment()
    