import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from etl.pipeline import run_etl

if __name__ == "__main__":
    run_etl()
    print("ETL process completed successfully.")