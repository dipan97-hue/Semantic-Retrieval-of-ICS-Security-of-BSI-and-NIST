from sentence_transformers import CrossEncoder

reranker  = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank_results(query, results , top_n =5):
    if not results:
        return[]
    
    pairs = []
    valid_results = []
    for r in results:
        content = r.get('content','')
        if not content:
            continue
        pairs.append([query, content])
        valid_results.append(r)

    if not pairs:
        return []
    scores = reranker.predict(pairs)

    for r, score in zip(valid_results,scores):
        r['rerank_score'] = float(score)

    reranked = sorted(valid_results,
                      key = lambda x:x["rerank_score"],
                      reverse=True)
    
    return reranked[:top_n]

