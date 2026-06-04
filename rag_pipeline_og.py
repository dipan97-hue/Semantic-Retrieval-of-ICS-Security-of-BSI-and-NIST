import requests
from sentence_transformers import SentenceTransformer

## Config

SUPABASE_URL = "https://kaueqrfosfzpdhtnwdko.supabase.co"
SUPABASE_KEY = "sb_publishable_xb-nsEG892PB_8CgyulR0w_T1MVv2Z9"

ollama_url = "http://localhost:11434/api/generate"
ollama_model = 'Llama3.1'
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}
model = SentenceTransformer('all-MiniLM-L6-v2')

## Embedding

def emb_query(text: str):
    return model.encode(text).tolist()

## Vector Retrieval


def retrieve(query_embedding, k):
    response = requests.post(
        f'{SUPABASE_URL}/rest/v1/rpc/match_requirements',
        headers=headers,
        json = {
            "query_embedding":query_embedding,
            "match_count": k
        }
    
    )

    return response.json()

def get_full_mappings(req_id):
    mapping_res = requests.get(
        f"{SUPABASE_URL}/rest/v1/requirement_mappings?source_requirement_id=eq.{req_id}",
        headers=headers
    ).json()

    mapped_data = []

    for m in mapping_res:
        score = m["similarity_score"]

        # 🔥 FILTER NOISE
        if score < 0.4:
            continue

        target_id = m["target_requirement_id"]

        req_res = requests.get(
            f"{SUPABASE_URL}/rest/v1/requirements_combined?id=eq.{target_id}",
            headers=headers
        ).json()

        if req_res:
            req = req_res[0]
            req["similarity_score"] = score

            # ADD LABEL
            if score > 0.55:
                req["mapping_strength"] = "strong"
            elif score > 0.4:
                req["mapping_strength"] = "medium"
            else:
                req["mapping_strength"] = "weak"

            mapped_data.append(req)

    return mapped_data


# =========================
#  BUILD CONTEXT (VERY IMPORTANT)
# =========================
def build_context(results):
    context = ""

    for r in results:
        context += f"[PRIMARY REQUIREMENT]\n"
        context += f"Title: {r['title']}\n"
        context += f"Content: {r['content']}\n\n"

        # Add mapped ones
        for m in r.get("mappings", []):
            context += f"[MAPPED REQUIREMENT | score={round(m['similarity_score'],2)}]\n"
            context += f"Title: {m['title']}\n"
            context += f"Content: {m['content']}\n\n"

    return context

# =========================
# EXPAND Query
# =========================

def expand_query(query):
    query_lower = query.lower()
    expansion_map = {
        "plc": [
            "plc", "ics", "scada", "industrial control system",
            "control system", "ot security"
        ],
        "remote": [
            "remote access", "external connection", "vpn",
            "remote authentication", "remote session"
        ],
        "backup": [
            "backup", "restore", "recovery",
            "continuity", "resilience", "redundancy"
        ],
        "segmentation": [
            "segmentation", "zone", "boundary",
            "isolation", "network separation"
        ],
        "access": [
            "access control", "authentication",
            "authorization", "identity", "privilege"
        ],
        "monitoring": [
            "monitoring", "logging", "alerting",
            "detection", "event analysis","vulnerability"
        ]
    }
    expanded_query = query
    for key, words in expansion_map.items():
        if key in query_lower:
            expanded_query+= " "+ " ".join(words)
    return expanded_query


# =========================
#  PROMPT
# =========================
def build_prompt(query, context):
    return f"""
You are a cybersecurity expert in industrial control systems (ICS).

Answer the question only using the retrieved context below.
If the context is insufficient, say: "Insufficient evidence in retrieved context."

Retrieved context:
{context}

User question:
{query}

Return your answer in this format:
1. Summary
2. Key security controls
3. BSI-NIST relationship in detail and in which part of the answer it is mentioned
4. Confidence (High/Medium/Low)
5. Similarity score of the retrieved requirements (if mentioned in the answer)

Rules:
- Do not invent information.
- Prefer concise and technical wording.
- Mention specific controls only if they appear in the context.

Answer:
"""

# =========================
# 🔹 OLLAMA CALL
# =========================
def generate_answer(prompt):
    response = requests.post(
        ollama_url,
        json={
            "model": ollama_model,
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code != 200:
        return "Error: Ollama not responding"

    return response.json()["response"]


# =========================
#  FULL RAG PIPELINE
# =========================
def rag(query, k=10):

    # Step 0: expanded query
    expanded_query = expand_query(query)
    print(f"Expanded query: {expanded_query}")
    # Step 1: embed query
    query_embedding = emb_query(expanded_query)

    # Step 2: retrieve requirements
    results = retrieve(query_embedding, k)

    # Step 3: enrich with mappings
    for r in results:
        r["mappings"] = get_full_mappings(r["id"])

    # Step 4: build context
    context = build_context(results)

    # Step 5: build prompt
    prompt = build_prompt(query, context)

    # Step 6: LLM generate
    answer = generate_answer(prompt)

    return {
        "query": query,
        "answer": answer,
        "results": results,
        "context": context
    }