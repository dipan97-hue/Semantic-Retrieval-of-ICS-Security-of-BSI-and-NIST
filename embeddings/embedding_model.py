import streamlit as st

from sentence_transformers import SentenceTransformer

# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer(
        "all-MiniLM-L6-v2",
        cache_folder="./models"
    )

model = load_embedding_model()
def emb_query(text: str):
    return model.encode(text).tolist()


