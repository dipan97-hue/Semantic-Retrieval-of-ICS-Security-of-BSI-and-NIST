import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st

try:
    if st.runtime.exists():

        supabase_url = st.secrets["supabase_url"]
        supabase_key = st.secrets["supabase_key"]
        gemini_api_key = st.secrets["gemini_api_key"]
        openai_api_key = st.secrets["openai_api_key"]
        anthropic_api_key = st.secrets["anthropic_api_key"]
        mistral_api_key = st.secrets["mistral_api_key"]
    else:
        raise Exception()

except:


    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")