import json 
from datetime import datetime 

def save_results(query, model_name, context, answer, results):

    data  = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "model_name": model_name,
        "context": context,
        "answer": answer,
        "results": results
    }

    with open('evalutation.jsonl', 'a', encoding='utf-8') as f:
        f.write(json.dumps(data) + '\n')

        