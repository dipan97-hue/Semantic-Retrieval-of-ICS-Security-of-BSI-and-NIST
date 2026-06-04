import sys
from pathlib import Path

# ---------------------------------------------------
# FIX IMPORT PATH
# ---------------------------------------------------
sys.path.insert(0,str(Path(__file__).parent.parent))

# ---------------------------------------------------
# IMPORTS
# ---------------------------------------------------
from storage.supabase_nist import upload_nist_data

from storage.supabase_bsi import upload_bsi_data

from storage.supabase_combined import upload_combined

from storage.supabase_mapping import upload_mappings

from etl.combined_dataset import (
    create_combined_dataset
)

from embeddings.embeddings import (
    add_embeddings
)

from embeddings.requirement_mapping import (
    create_requirement_mappings
)


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------
if __name__ == "__main__":

    # ---------------------------------------------------
    # Upload individual datasets
    # ---------------------------------------------------
    print("Uploading BSI dataset...")
    #upload_bsi_data()

    print("Uploading NIST dataset...")
    #upload_nist_data()

    # ---------------------------------------------------
    # Build combined dataset
    # ---------------------------------------------------
    print("Building combined dataset...")

    combined_rows = create_combined_dataset(
        r"D:\exercises\Thesis\Json Files\bsi_standard.json",
        r"D:\exercises\Thesis\Json Files\Nist_Standard.json"
    )

    print(f"Combined rows: {len(combined_rows)}")

    # ---------------------------------------------------
    # Add embeddings
    # ---------------------------------------------------
    print("Creating embeddings...")

    combined_rows = add_embeddings(
        combined_rows
    )

    print("Embeddings completed")

    # ---------------------------------------------------
    # Upload combined dataset
    # ---------------------------------------------------
    print("Uploading combined dataset...")

    upload_combined(combined_rows)

    # ---------------------------------------------------
    # Create mappings
    # ---------------------------------------------------
    print("Creating mappings...")

    mappings = create_requirement_mappings( combined_rows)

    print(f"Mappings created: {len(mappings)}")

    # ---------------------------------------------------
    # Upload mappings
    # ---------------------------------------------------
    print("Uploading mappings...")

    upload_mappings(mappings)

    print("Pipeline completed successfully")