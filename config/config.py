import os
from dotenv import load_dotenv

load_dotenv()

import streamlit as st

try:

    if st.runtime.exists():

        SUPABASE_URL = st.secrets["SUPABASE_URL"]
        SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
        OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
        ANTHROPIC_API_KEY = st.secrets["ANTHROPIC_API_KEY"]
        MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]

    else:

        raise Exception()

except:

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")