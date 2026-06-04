from config.config import (
    SUPABASE_URL,
    SUPABASE_KEY
)

import requests


# =====================================================
# HEADERS
# =====================================================
headers = {

    "apikey": SUPABASE_KEY,

    "Authorization":
        f"Bearer {SUPABASE_KEY}",

    "Content-Type":
        "application/json"
}


# =====================================================
# RETRIEVE NIST + BSI BALANCED
# =====================================================
def retrieve(

    query_embedding,

    k=10

):

    # =============================================
    # SPLIT K
    # =============================================
    per_standard = max(1, k // 2)

    # =============================================
    # NIST RETRIEVAL
    # =============================================
    nist_response = requests.post(

        f"{SUPABASE_URL}/rest/v1/rpc/"
        f"match_requirements",

        headers=headers,

        json={

            "query_embedding":
                query_embedding,

            "match_count":
                per_standard,

            "filter_standard":
                "NIST"
        }
    )

    # =============================================
    # BSI RETRIEVAL
    # =============================================
    bsi_response = requests.post(

        f"{SUPABASE_URL}/rest/v1/rpc/"
        f"match_requirements",

        headers=headers,

        json={

            "query_embedding":
                query_embedding,

            "match_count":
                per_standard,

            "filter_standard":
                "BSI"
        }
    )

    # =============================================
    # PARSE
    # =============================================
    nist_results = nist_response.json()

    bsi_results = bsi_response.json()

    # =============================================
    # COMBINE
    # =============================================

    if isinstance(nist_results, dict):

        print("NIST ERROR:", nist_results)

        nist_results = []

    if isinstance(bsi_results, dict):

        print("BSI ERROR:", bsi_results)

        bsi_results = []

    results = nist_results + bsi_results


    # =============================================
    # SORT BY SIMILARITY
    # =============================================
    results = sorted(

        results,

        key=lambda x:
            x["similarity"],

        reverse=True
    )

    return results