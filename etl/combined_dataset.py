import json

from etl.cleaning import is_noise_title
from etl.save_json import save_json


# ---------------------------------------------------
# CREATE COMBINED DATASET
# ---------------------------------------------------
def create_combined_dataset(
    bsi_json,
    nist_json
):

    combined_rows = []

    # ---------------------------------------------------
    # LOAD JSON FILES
    # ---------------------------------------------------
    with open(
        bsi_json,
        "r",
        encoding="utf-8"
    ) as f:

        bsi_data = json.load(f)

    with open(
        nist_json,
        "r",
        encoding="utf-8"
    ) as f:

        nist_data = json.load(f)

    print("BSI loaded:", len(bsi_data))
    print("NIST loaded:", len(nist_data))

    # ---------------------------------------------------
    # BSI DATA
    # ---------------------------------------------------
    for item in bsi_data:

        title = item.get("title", "")

        if is_noise_title(title):
            continue

        combined_rows.append({

            "source_standard": "BSI",

            "source_id":
                item.get("source_id"),

            "section_number":
                item.get("section_number"),

            "chunk_id":
                item.get("chunk_id"),

            "title":
                item.get("title"),

            "parent":
                item.get("parent"),

            "content":
                item.get("content"),

            "summary":
                item.get("summary"),

            "lifecycle_phase":
                item.get("lifecycle_phase"),

            "normative":
                item.get("normative"),

            "normative_type":
                item.get("normative_type"),

            "keywords":
                item.get("keywords") or [],

            "abstraction_level":
                "governance"
        })

    print(
        "Combined after BSI:",
        len(combined_rows)
    )

    # ---------------------------------------------------
    # NIST DATA
    # ---------------------------------------------------
    for item in nist_data:

        title = item.get("title", "")

        if is_noise_title(title):
            continue

        combined_rows.append({

            "source_standard": "NIST",

            "source_id":
                item.get("source_id"),

            "section_number":
                item.get("section_number"),

            "chunk_id":
                item.get("chunk_id"),

            "title":
                item.get("title"),

            "parent":
                item.get("parent"),

            "content":
                item.get("content"),

            "summary":
                item.get("summary"),

            "lifecycle_phase":
                item.get("lifecycle_phase"),

            "normative":
                item.get("normative"),

            "normative_type":
                item.get("normative_type"),

            "keywords":
                item.get("keywords") or [],

            "abstraction_level":
                "technical"
        })

    print(
        "Combined after NIST:",
        len(combined_rows)
    )

    # ---------------------------------------------------
    # SAVE JSON
    # ---------------------------------------------------
    output_path = (
        r"D:\exercises\Thesis\Json Files"
        r"\combined_dataset.json"
    )

    save_json(
        combined_rows,
        output_path
    )

    print(
        f"Saved JSON to {output_path}"
    )

    print(
        f"Combined rows: "
        f"{len(combined_rows)}"
    )

    return combined_rows