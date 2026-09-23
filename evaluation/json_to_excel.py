import json

import pandas as pd
from openpyxl import Workbook
import os 

input_file = r'D:\exercises\Thesis\results\cross_model_results.json'
output_file = r'D:\exercises\Thesis\results\cross_model_results.xlsx'

categories = [
    "relevance",
    "technical_accuracy",
    "faithfulness",
    "completeness",
    "ot_operational_suitability",
    "bsi_nist_alignment",
    "hallucination_risk",
    "overall_quality"
]

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

detailed_rows = []

for query_item in data:
    query_id = query_item.get('query_id')
    category = query_item['category']
    query = query_item['query']
    for evaluation in query_item.get('evaluations', []):
        if evaluation.get('score') is None:
            continue
        hallucination_risk = evaluation.get('hallucination_risk')
        hallucination_normalized = (6 - float(hallucination_risk))

        ## Calculate final score 
        scores = [

            float(
                evaluation.get(
                    "relevance",
                    0
                )
            ),

            float(
                evaluation.get(
                    "technical_accuracy",
                    0
                )
            ),

            float(
                evaluation.get(
                    "faithfulness",
                    0
                )
            ),

            float(
                evaluation.get(
                    "completeness",
                    0
                )
            ),

            float(
                evaluation.get(
                    "ot_operational_suitability",
                    0
                )
            ),

            float(
                evaluation.get(
                    "bsi_nist_alignment",
                    0
                )
            ),

            hallucination_normalized,

            float(
                evaluation.get(
                    "overall_quality",
                    0
                )
            )
        ]


        final_score = sum(scores) / len(scores)


        detailed_rows.append({

            "query_id": query_id,

            "category": category,

            "query": query,

            "candidate_model": evaluation.get(
                "candidate_model"
            ),

            "top_k": evaluation.get(
                "top_k"
            ),

            "judge_model": evaluation.get(
                "judge_model"
            ),

            "relevance": evaluation.get(
                "relevance"
            ),

            "technical_accuracy": evaluation.get(
                "technical_accuracy"
            ),

            "faithfulness": evaluation.get(
                "faithfulness"
            ),

            "completeness": evaluation.get(
                "completeness"
            ),

            "ot_operational_suitability":evaluation.get("ot_operational_suitability"),

            "bsi_nist_alignment": evaluation.get("bsi_nist_alignment"),

            "hallucination_risk":evaluation.get("hallucination_risk"),

            "hallucination_normalized":
                hallucination_normalized,

            "overall_quality":
                evaluation.get(
                    "overall_quality"
                ),

            "final_score":
                round(
                    final_score,
                    3
                ),

            "reason":
                evaluation.get(
                    "reason",
                    ""
                )
        })


# ============================================================
# CREATE DATAFRAME
# ============================================================


detailed_df = pd.DataFrame(detailed_rows)


# ============================================================
# QUERY + MODEL + K RANKING
# ============================================================

query_config_df = (

    detailed_df

    .groupby(
        [
            "query_id",
            "category",
            "candidate_model",
            "top_k"
        ],
        as_index=False
    )

    .agg(

        judge_count=(
            "final_score",
            "count"
        ),

        average_score=(
            "final_score",
            "mean"
        )

    )
)


query_config_df["average_score"] = (
    query_config_df["average_score"]
    .round(3)
)


# ============================================================
# RANK WITHIN EACH QUERY
# ============================================================

query_config_df["rank"] = (

    query_config_df

    .groupby("query_id")[
        "average_score"
    ]

    .rank(
        method="min",
        ascending=False
    )

    .astype(int)
)


query_config_df = query_config_df[
    [
        "query_id",
        "category",
        "candidate_model",
        "top_k",
        "judge_count",
        "average_score",
        "rank"
    ]
]


# ============================================================
# OVERALL MODEL + K RANKING
# ============================================================

overall_df = (

    query_config_df

    .groupby(
        [
            "candidate_model",
            "top_k"
        ],
        as_index=False
    )

    .agg(

        average_score=(
            "average_score",
            "mean"
        ),

        query_count=(
            "query_id",
            "nunique"
        )

    )
)


overall_df["average_score"] = (
    overall_df["average_score"]
    .round(3)
)


overall_df = overall_df.sort_values(
    "average_score",
    ascending=False
).reset_index(
    drop=True
)


overall_df.insert(
    0,
    "rank",
    range(
        1,
        len(overall_df) + 1
    )
)


# ============================================================
# TOP-K RANKING
# ============================================================

top_k_df = (

    query_config_df

    .groupby(
        "top_k",
        as_index=False
    )

    .agg(

        average_score=(
            "average_score",
            "mean"
        ),

        query_count=(
            "query_id",
            "nunique"
        )

    )
)


top_k_df["average_score"] = (
    top_k_df["average_score"]
    .round(3)
)


top_k_df = top_k_df.sort_values(
    "average_score",
    ascending=False
).reset_index(
    drop=True
)


top_k_df.insert(
    0,
    "rank",
    range(
        1,
        len(top_k_df) + 1
    )
)


# ============================================================
# BEST CONFIGURATION PER QUERY
# ============================================================

best_per_query_df = (

    query_config_df

    .sort_values(
        [
            "query_id",
            "average_score"
        ],
        ascending=[
            True,
            False
        ]
    )

    .groupby(
        "query_id",
        as_index=False
    )

    .first()
)


best_per_query_df = best_per_query_df[
    [
        "query_id",
        "category",
        "candidate_model",
        "top_k",
        "average_score"
    ]
]


# ============================================================
# SAVE EXCEL
# ============================================================

os.makedirs(os.path.dirname(output_file), exist_ok=True)


with pd.ExcelWriter(output_file, engine="openpyxl") as writer:


    detailed_df.to_excel(writer,sheet_name="Detailed_Evaluations",index=False)

    query_config_df.to_excel(
        writer,
        sheet_name="Query_Config_Ranking",
        index=False
    )

    overall_df.to_excel(
        writer,
        sheet_name="Overall_Ranking",
        index=False
    )

    top_k_df.to_excel(
        writer,
        sheet_name="Top_K_Ranking",
        index=False
    )

    best_per_query_df.to_excel(
        writer,
        sheet_name="Best_Per_Query",
        index=False
    )


print("\nExcel analysis completed.")

print(
    f"Saved to: {output_file}"
)


# ============================================================
# PRINT BEST RESULT
# ============================================================

if not overall_df.empty:

    best = overall_df.iloc[0]

    print("\nBEST CONFIGURATION")
    print("---------------------------")

    print(
        f"Model: {best['candidate_model']}"
    )

    print(
        f"Top-K: {best['top_k']}"
    )

    print(
        f"Average Score: {best['average_score']}"
    )

       