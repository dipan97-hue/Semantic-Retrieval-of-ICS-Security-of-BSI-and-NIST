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

