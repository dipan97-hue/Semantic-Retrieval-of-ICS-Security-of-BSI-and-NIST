from config.config import SUPABASE_URL, SUPABASE_KEY
import requests
import json

INSERT_BATCH_SIZE = 100

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def clear_table(table_name):
    delete_url = (
        f"{SUPABASE_URL}/rest/v1/"
        f"{table_name}?chunk_id=neq.null"
    )
    response = requests.delete(delete_url, headers=headers)
    return response

def load_json(json_path):
    with open(json_path,"r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def transform_nist_rows(data):

    rows = []

    for item in data:

        standard = item.get("standard", {})

        rows.append({
        "chunk_id": item.get("chunk_id"),

        "standard_name": item.get("source_standard"),  
        "version": "1.0",                              
        "year": 2023,                                 
        "type": "technical",                          

        "source_id": item.get("source_id"),
        "section_number": item.get("section_number"),
        "title": item.get("title"),
        "parent": item.get("parent"),

        "lifecycle_phase": item.get("lifecycle_phase"),
        "normative": item.get("normative"),
        "normative_type": item.get("normative_type"),

        "keywords": item.get("keywords") or [],
        "summary": item.get("summary"),
        "content": item.get("content"),
        })

    return rows


# ---------------------------------------------------
# INSERT INTO SUPABASE
# ---------------------------------------------------
def insert_rows(table_name, rows):

    url = f"{SUPABASE_URL}/rest/v1/{table_name}"

    for start in range(0, len(rows), INSERT_BATCH_SIZE):
        batch = rows[start:start + INSERT_BATCH_SIZE]

        response = requests.post(
            url,
            headers=headers,
            json=batch
        )

        print(
            f"INSERT {table_name} "
            f"{start + 1}-{start + len(batch)}: "
            f"{response.status_code}"
        )

        print(response.text)

def upload_nist_data():

    table_name = 'nist_standard' 
    
    json_path = r'D:\exercises\Thesis\Json Files\nist_standard.json'

    data = load_json(json_path)

    rows = transform_nist_rows(data)
    ## Clear existing data before inserting new rows
    clear_table(table_name)
    ## Insert new rows
    insert_rows(table_name, rows)

    print(f"NIST data upload completed. Total rows inserted: {len(rows)}")


    