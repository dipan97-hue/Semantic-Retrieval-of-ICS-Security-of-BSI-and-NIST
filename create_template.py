import os 
from pathlib import Path
import logging
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

list_of_files =[
    'README.md',
    'requirements.txt',
    f'etl/common.py',
    f'etl/chunking.py',
    f'etl/cleaning.py',
    f'etl/lifecycle_bsi.py',
    f'etl/lifecycle_nist.py',
    f'etl/pipeline.py',
    'app.py',
    f'config/config.py',
    f'.env',
    f'etl/bsi_extract.py',
    f'etl/nist_extract.py',
    f'storage/supabase_bsi.py', 
    f'storage/supabase_nist.py',
    f'etl/save_json.py',
    f'Runs/run_db.py'
    f'storage/__init__.py',
    f'etl/__init__.py',
    f'etl/combined_dataset.py',
    f'embeddings/__init__.py',
    f'embeddings/embeddings.py',
    'tests.sql',
    f'retrieval/retrieve.py',
    f'retrieval/mappings.py',
    f'retrieval/query_expansion.py',
    f'retrieval/context_building.py',
    f'llm/gpt_llm.py',
    f'llm/gemini_llm.py',
    f'llm/mistral_llm.py',
    f'llm/llm_router.py',
    f'prompts/prompt_builder.py',
    f'rag/rag_pipeline.py',
    'project_structure.txt',
    f'evaluation/ares.py',
    f'evaluation/metrics.py',
    'gitignore'
    
    
]   

for file in list_of_files:
    filepath = Path(file)
    filedir, filename = os.path.split(filepath)
    if not os.path.exists(filedir) and filedir!= '':
        os.makedirs(filedir)
        
        logging.info(f"Directory created: {filedir}")
    
    if not os.path.exists(filepath):
        with open(filepath, 'w') as file:
            pass
        logging.info(f"File created: {filepath}")
    else:
        logging.info(f"File already exists: {filename}")
