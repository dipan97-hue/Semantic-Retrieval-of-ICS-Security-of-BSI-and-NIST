import pandas as pd

# Load your CSV
df = pd.read_csv("evaluation\\llm_judge_results.csv")

if "hallucination_quality" not in df.columns and "hallucination_risk" in df.columns:
    df["hallucination_quality"] = 6 - df["hallucination_risk"]

# Metrics
metrics = [
    "relevance",
    "faithfulness",
    "hallucination_risk",
    "technical_accuracy",
    "context_utilization"
]


# --------------------------------------------------
# Calculate average for each model
# --------------------------------------------------

model_summary = (
    df.groupby("model")
    .agg(
        Relevance=("relevance", "mean"),
        Faithfulness=("faithfulness", "mean"),
        Hallucination_Risk=("hallucination_risk", "mean"),
        Technical_Accuracy=("technical_accuracy", "mean"),
        Context_Use=("context_utilization", "mean"),
        Hallucination_Quality=("hallucination_quality", "mean")
    )
    .reset_index()
)

# --------------------------------------------------
# Overall average
# IMPORTANT:
# Use hallucination_quality, not raw hallucination_risk
# --------------------------------------------------

model_summary["Overall_Avg"] = model_summary[
    [
        "Relevance",
        "Faithfulness",
        "Hallucination_Quality",
        "Technical_Accuracy",
        "Context_Use"
    ]
].mean(axis=1)

# Round values
model_summary = model_summary.round(2)

# --------------------------------------------------
# Rename columns for display
# --------------------------------------------------

model_summary = model_summary.rename(
    columns={
        "model": "Model",
        "Hallucination_Risk": "Hallucination Risk",
        "Technical_Accuracy": "Technical Accuracy",
        "Context_Use": "Context Use",
        "Overall_Avg": "Overall Avg"
    }
)

# Remove Hallucination Quality from display
model_summary = model_summary[
    [
        "Model",
        "Relevance",
        "Faithfulness",
        "Hallucination Risk",
        "Technical Accuracy",
        "Context Use",
        "Overall Avg"
    ]
]
df1 = pd.DataFrame(model_summary)
print(df1.to_string(index=False))
#print(model_summary.to_string(index=False))