import json
import re
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rag.rag_pipeline import rag



# =====================================================
# MODELS
# =====================================================

MODELS = [
    "gpt-5.4-nano",
    "gemini-3.1-flash-lite",
    "claude-haiku-4-5",
    "Mistral"
]


# =====================================================
# QUERIES
# =====================================================

QUERIES = [

    "How should PLCs be authenticated in OT environments? ",
    "What security controls should be applied to PLC programming interfaces? ",
    "How should user authentication be implemented in ICS systems? ",

    "What authentication mechanisms are recommended for OT environments?",
    "How should OT backups be protected? ",
    "What recovery procedures should be established for industrial systems? ",
    "What security requirements apply to SCADA systems? ",
    "How should ICS assets be identified and managed? "

    
]


def extract_score(metric, text):

    match = re.search(
        rf"{re.escape(metric)}:\s*(\d+)/5",
        text,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    return None


all_results = []

for model in MODELS:

    print(f"\nRunning model: {model}")

    for query in QUERIES:

        print(f"Query: {query}")

        try:

            result = rag(
                query=query,
                model_name=model
            )

            evaluation = result["evaluation_output"]

            record = {

                "timestamp": datetime.now().isoformat(),

                "model": model,

                "query": query,

                "answer": result["answer"],

                "relevance":
                    extract_score(
                        "Relevance",
                        evaluation
                    ),

                "faithfulness":
                    extract_score(
                        "Faithfulness",
                        evaluation
                    ),

                "hallucination_risk":
                    extract_score(
                        "Hallucination Risk",
                        evaluation
                    ),

                "technical_accuracy":
                    extract_score(
                        "Technical Accuracy",
                        evaluation
                    ),

                "context_utilization":
                    extract_score(
                        "Context Utilization",
                        evaluation
                    )
            }

            all_results.append(record)

            print("SUCCESS")

        except Exception as e:

            print(f"ERROR: {e}")

            all_results.append({

                "timestamp": datetime.now().isoformat(),

                "model": model,

                "query": query,

                "error": str(e)
            })


with open(
    f"evaluation/llm_judge_results.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_results,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nFinished.")
print(f"Total evaluations: {len(all_results)}")

df = pd.DataFrame(all_results)
df.to_csv("evaluation/llm_judge_results.csv", encoding="utf-8", index=False)
