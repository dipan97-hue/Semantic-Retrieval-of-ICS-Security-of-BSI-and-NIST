from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------------------------
# LIFECYCLE MAP
# ---------------------------------------------------
lifecycle_map = {
    "Plan": "Identify",
    "Do": "Protect",
    "Check": "Detect",
    "Act": "Respond"
}


# ---------------------------------------------------
# CREATE MAPPINGS
# ---------------------------------------------------
def create_requirement_mappings(rows):

    bsi_rows = [
        r for r in rows
        if r["source_standard"] == "BSI"
    ]

    nist_rows = [
        r for r in rows
        if r["source_standard"] == "NIST"
    ]

    mappings = []

    for bsi in bsi_rows:

        best_match = None

        best_score = 0

        best_lifecycle_match = False

        bsi_phase = bsi.get(
            "lifecycle_phase"
        )

        for nist in nist_rows:

            nist_phase = nist.get(
                "lifecycle_phase"
            )

            sim = cosine_similarity(
                [bsi["embedding"]],
                [nist["embedding"]]
            )[0][0]

            lifecycle_match = False

            if bsi_phase in lifecycle_map:

                if (lifecycle_map[bsi_phase] == nist_phase):

                    lifecycle_match = True

                    sim += 0.05

            if sim > best_score:

                best_score = sim

                best_match = nist

                best_lifecycle_match = lifecycle_match

        if best_match:

            mappings.append({

                "source_requirement_id":
                    bsi["chunk_id"],

                "target_requirement_id":
                    best_match["chunk_id"],

                "similarity_score":
                    float(best_score),

                "lifecycle_match":
                    best_lifecycle_match
            })

    return mappings