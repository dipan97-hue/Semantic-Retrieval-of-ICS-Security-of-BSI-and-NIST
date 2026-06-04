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
1. Summary: with most relevant information from the retrieved context
2. Key security controls
3. Confidence (High/Medium/Low) 
4. Explain why you are confident or not confident, based strictly on the retrieved context.
If confidence is not High, add a short explanation of what is missing or unclear.

Rules:
- No hallucinations
- Do not invent information.
- Prefer concise and technical wording.
- Mention specific controls only if they appear in the context.

Answer:
"""