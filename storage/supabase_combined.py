from config.config import SUPABASE_URL, SUPABASE_KEY
import requests
import json

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def upload_combined(rows):
    table_name = 'requirements_combined'
    url = f"{SUPABASE_URL}/rest/v1/{table_name}"

    delete_response = requests.delete(
    url + "?chunk_id=neq.null",
    headers=headers
    )   
    print("DELETE:", delete_response.status_code)

    insert_response = requests.post(url, headers=headers, data=json.dumps(rows))
    print("INSERT:", insert_response.status_code, insert_response.text)


