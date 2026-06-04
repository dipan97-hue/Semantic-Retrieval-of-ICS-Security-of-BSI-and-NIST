import requests

from config.config import (
    SUPABASE_URL,
    SUPABASE_KEY
)

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}


# ---------------------------------------------------
# UPLOAD MAPPINGS
# ---------------------------------------------------
def upload_mappings(mappings):

    table = "requirement_mappings"

    url = f"{SUPABASE_URL}/rest/v1/{table}"

    # DELETE OLD
    delete_response = requests.delete(
        url + "?id=neq.0",
        headers=headers
    )

    print("DELETE:", delete_response.status_code)

    # INSERT
    response = requests.post(url,headers=headers,json=mappings)

    print(
        "INSERT:",
        response.status_code
    )

    print(response.text)