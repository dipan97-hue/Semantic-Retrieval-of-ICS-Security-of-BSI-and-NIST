from sentence_transformers import SentenceTransformer

# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')

# ---------------------------------------------------
# CREATE EMBEDDING
# ---------------------------------------------------
def create_embedding(row):

    text = f"""
    {row['title']}
    {row['summary']}
    {row['content']}
    {row['keywords']}
    {row['lifecycle_phase']}
    {row['normative_type']}
    """

    embedding = model.encode(text)

    return embedding.tolist()


# ---------------------------------------------------
# ADD EMBEDDINGS
# ---------------------------------------------------
def add_embeddings(rows):

    for i, row in enumerate(rows):

        #print(f"Embedding {i+1}/{len(rows)}"))

        row["embedding"] = create_embedding(row)

    return rows