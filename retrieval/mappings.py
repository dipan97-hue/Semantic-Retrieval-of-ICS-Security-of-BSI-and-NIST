from config.config import (
    SUPABASE_KEY,
    SUPABASE_URL
)

import requests


# =====================================================
# HEADERS
# =====================================================
headers = {

    "apikey": SUPABASE_KEY,

    "Authorization":f"Bearer {SUPABASE_KEY}",

    "Content-Type":"application/json"
}


# =====================================================
# GET FULL BSI ↔ NIST MAPPINGS
# =====================================================
def get_full_mappings(req_id):

    # =============================================
    # CLEAN INPUT
    # =============================================
    req_id = str(req_id).strip()

    mapped_data = []

    # =============================================
    # FETCH BOTH DIRECTIONS
    # =============================================
    mapping_res = requests.get(

        f"{SUPABASE_URL}/rest/v1/"
        f"requirement_mappings?"
        f"or=("
        f"source_requirement_id.eq.{req_id},"
        f"target_requirement_id.eq.{req_id}"
        f")",

        headers=headers

    ).json()

    # print("===================================")
    # print("REQ ID:", req_id)
    # print("MAPPINGS:", mapping_res)
    # print("===================================")

    # =============================================
    # IF ERROR FROM SUPABASE
    # =============================================
    if isinstance(mapping_res, dict):

        print("SUPABASE ERROR:", mapping_res)

        return []

    # =============================================
    # LOOP THROUGH MAPPINGS
    # =============================================
    for m in mapping_res:

        score = float(m.get( "similarity_score",0))

        # =========================================
        # MINIMUM THRESHOLD = 10%
        # =========================================
        if score < 0.10:

            continue

        source_id = str(
            m.get(
                "source_requirement_id",
                ""
            )
        ).strip()

        target_id = str(
            m.get(
                "target_requirement_id",
                ""
            )
        ).strip()

        # =========================================
        # DETERMINE RELATED CHUNK
        # =========================================
        if req_id == source_id:

            related_id = target_id

        else:

            related_id = source_id

        # =========================================
        # FETCH RELATED REQUIREMENT
        # =========================================
        req_res = requests.get(

            f"{SUPABASE_URL}/rest/v1/"
            f"requirements_combined?"
            f"chunk_id=eq.{related_id}",

            headers=headers

        ).json()

        # =========================================
        # IF FOUND
        # =========================================
        if req_res and isinstance(req_res, list):

            req = req_res[0]

            # =====================================
            # ADD SIMILARITY
            # =====================================
            req["similarity_score"] = round(
                score,
                3
            )

            # =====================================
            # MAPPING STRENGTH
            # =====================================
            if score >= 0.75:

                strength = "Very Strong"

            elif score >= 0.60:

                strength = "Strong"

            elif score >= 0.45:

                strength = "Medium"

            elif score >= 0.20:

                strength = "Weak"

            else:

                strength = "Very Weak"

            req["mapping_strength"] = strength

            mapped_data.append(req)

    # =============================================
    # REMOVE DUPLICATES
    # =============================================
    unique_results = []

    seen = set()

    for item in mapped_data:

        cid = item.get(
            "chunk_id"
        )

        if cid not in seen:

            unique_results.append(item)

            seen.add(cid)

    # =============================================
    # SORT BY SIMILARITY
    # =============================================
    unique_results = sorted(

        unique_results,

        key=lambda x:
            x.get(
                "similarity_score",
                0
            ),

        reverse=True
    )

    # print("===================================")
    # print("FINAL MAPPINGS:")
    # print(unique_results)
    # print("===================================")

    return unique_results