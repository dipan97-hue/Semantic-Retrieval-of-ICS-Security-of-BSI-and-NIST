import streamlit as st
import pandas as pd

from rag.rag_pipeline import rag
from llm.role_generator import generate_role, usecase_generation
from llm.llm_judge import evaluate_complete_rag as evaluate_rag_response
import os
import warnings
import logging

# =====================================================
# SUPPRESS WARNINGS
# =====================================================

warnings.filterwarnings("ignore")

warnings.simplefilter(action="ignore", category=FutureWarning)

warnings.simplefilter(action="ignore",category=UserWarning)

# =====================================================
# TRANSFORMERS WARNINGS
# =====================================================

logging.getLogger(
    "transformers"
).setLevel(logging.ERROR)

logging.getLogger(
    "sentence_transformers"
).setLevel(logging.ERROR)

logging.getLogger(
    "huggingface_hub"
).setLevel(logging.ERROR)

# =====================================================
# HIDE HF / TORCH WARNINGS
# =====================================================

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

os.environ["TRANSFORMERS_VERBOSITY"] = "error"

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# =====================================================
# OPTIONAL
# =====================================================

os.environ["PYTHONWARNINGS"] = "ignore"

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="OT Security RAG Platform",
    page_icon="🛡️",
    layout="wide"
)

# =====================================================
# MAIN TITLE
# =====================================================
st.title("🛡️ Intelligent OT Security & Governance " 
         "Requirements Analysis Platform")

st.markdown("""
AI-powered Retrieval-Augmented Generation (RAG) platform for:

- NIST SP 800-82
- BSI IT-Grundschutz
- ICS / SCADA Cybersecurity
- Semantic Requirement Mapping
- Multi-LLM Security Analysis
""")

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("⚙️ Settings")

model_name = st.sidebar.selectbox(
    "Select LLM",
    [
        "claude-sonnet-4.6",
        "Mistral",
        "gemini-3.1-flash-lite",
        "gpt-5.4-nano"

    ]
)

k = st.sidebar.slider(
    "Top-K Retrieval",
    min_value=1,
    max_value=30,
    value=10
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation:",
    [
        "🤖 OT Security Assistant",
       "🔗 Knowledge Base",
       "👤 Generate Roles",
       "📊 Generate Use Cases",
        "🧠 Multi-LLM Comparison",
        "⚖️ LLM Judge"
       
    ])
st.sidebar.markdown("---")
## Adding a clear button to reset session state and clear results
if st.sidebar.button(
    "🗑️ Clear Session",
    use_container_width=True
):
    for key in list(
        st.session_state.keys()
    ):

        del st.session_state[key]

    st.rerun()

if page == "🤖 OT Security Assistant" :
    st.header("OT Security Requirements Assistant")

    st.markdown("""
Ask cybersecurity questions related to:

- PLC Security
- Authentication
- Backup & Recovery
- ICS / SCADA
- Network Segmentation
- Monitoring
- OT Security Controls
- Governance
""")

    # =====================================
    # QUERY INPUT
    # =====================================
    query = st.text_area(
        "Enter your query",
        height=150
    )

    # =====================================
    # RUN ANALYSIS
    # =====================================
    if st.button("Run Analysis"):

        if not query.strip():

            st.warning(
                "Please enter a query."
            )

        else:

            with st.spinner(
                "Running your query, please wait..."
            ):

                result = rag(
                    query=query,
                    model_name=model_name,
                    k=k
                )

            # SAVE RESULTS
            st.session_state["rag_results"] = result

    # =====================================
    # SHOW GENERATED ANSWER
    # =====================================
    if "rag_results" in st.session_state:

        result = st.session_state["rag_results"]

        st.subheader("📌 Generated Security Analysis")

        st.write(result["answer"])

# =====================================
# # AI INSIGHTS
# =====================================
if page == "👤 Generate Roles" :
    if "rag_results" not in st.session_state:

        st.info("Run a query first from the OT Security Assistant page.")
    else:

        query = st.session_state["rag_results"].get("query", "")

        st.subheader("🧠 AI-Powered Operational Insights")

        st.markdown("""
                    Generate OT cybersecurity roles,
                    industrial use cases,
                    and operational interpretations
                    from retrieved requirements.
                    """)

        if st.button("Generate Role Analysis"):

            with st.spinner("Generating role analysis..."):

                role_output = generate_role(
                    query=query,
                    results=st.session_state["rag_results"]["results"],
                    model_name=model_name
                )

                st.session_state["role_output"] = role_output

        if "role_output" in st.session_state:

            st.write(st.session_state["role_output"])    

    # =====================================
    # USECASE GENERATION
    # =====================================
    
if page == "📊 Generate Use Cases" :
        st.header("📊 OT Security Use Case Generation" )
        if "rag_results" not in st.session_state:
            st.info("Run a query first from the OT Security Assistant page.")
        else:

            query = st.session_state["rag_results"].get("query", "")

            if st.button("Generate Use Cases"):

                with st.spinner("Generating use cases..."):

                    usecase_output = usecase_generation(
                        query=query,
                        results=st.session_state["rag_results"]["results"],
                        model_name=model_name
                    )

                    st.session_state["usecase_output"] = usecase_output 
                    
            if "usecase_output" in st.session_state:

                st.write(st.session_state["usecase_output"]) 
            

# =====================================================
# TAB 2 — KNOWLEDGE BASE
# =====================================================
if page == "🔗 Knowledge Base" :

    st.header("📚 OT Security Knowledge Base")

    st.markdown("""
Explore retrieved OT cybersecurity
requirements, their originating standards,
and semantic relationships between
BSI and NIST.
""")

    # =================================================
    # CHECK RESULTS
    # =================================================
    if "rag_results" not in st.session_state:

        st.info("Run a query first from the OT Security Assistant tab.")

    else:

        result = st.session_state["rag_results"]

        # =================================================
        # LOOP THROUGH RETRIEVED RESULTS
        # =================================================
        for idx, r in enumerate(result["results"]):

            mappings = r.get("mappings",[])

            # =================================================
            # EXPANDER
            # =================================================
            with st.expander(f"{idx+1}. "
                             f"{r['title']}"):

                # =============================================
                # PRIMARY REQUIREMENT
                # =============================================
                st.markdown(f"## 📄 "
                            f"{r['source_standard']}")

                st.markdown("### Extracted Requirement")

                st.write( r["content"])

                st.markdown("---")

                # =============================================
                # PRIMARY METADATA
                # =============================================
                col1, col2, col3 = st.columns(3)

                # -----------------------------------------
                # LIFECYCLE
                # -----------------------------------------
                with col1:

                    st.markdown(
                        f"**Lifecycle Phase**  \n"
                        f"{r.get('lifecycle_phase', 'None')}"
                    )

                # -----------------------------------------
                # NORMATIVE
                # -----------------------------------------
                with col2:

                    st.markdown(
                        f"**Normative Type**  \n"
                        f"{r.get('normative_type', 'None')}"
                    )

                # -----------------------------------------
                # SIMILARITY
                # -----------------------------------------
                with col3:

                    if mappings:

                        similarity = round(

                            mappings[0].get(
                                "similarity_score",
                                0
                            ),

                            3
                        )

                    else:

                        similarity = 0

                    st.markdown(
                        f"**BSI ↔ NIST Similarity**  \n"
                        f"{similarity}"
                    )

                # =============================================
                # RELATED REQUIREMENTS
                # =============================================
                st.markdown("---")

                st.markdown("## 🔗 Related Requirement")

                # =============================================
                # IF MAPPINGS EXIST
                # =============================================
                if mappings:

                    for m in mappings:

                        similarity = round(m.get( "similarity_score",0),3)

                        # =====================================
                        # RELATED STANDARD
                        # =====================================
                        st.success(

                            f"{m['source_standard']} "
                            f"relationship found "
                            f"(Similarity: {similarity})"

                        )

                        # =====================================
                        # RELATED TITLE
                        # =====================================
                        st.markdown(

                            f"### {m['title']}"

                        )

                        # =====================================
                        # RELATED CONTENT
                        # =====================================
                        st.write(

                            m["content"]

                        )

                        # =====================================
                        # RELATED METADATA
                        # =====================================
                        col4, col5, col6 = st.columns(3)

                        # ---------------------------------
                        # LIFECYCLE
                        # ---------------------------------
                        with col4:

                            st.markdown(
                                f"**Lifecycle**  \n"
                                f"{m.get('lifecycle_phase', 'None')}"
                            )

                        # ---------------------------------
                        # NORMATIVE
                        # ---------------------------------
                        with col5:

                            st.markdown(
                                f"**Normative**  \n"
                                f"{m.get('normative_type', 'None')}"
                            )

                        # ---------------------------------
                        # STRENGTH
                        # ---------------------------------
                        with col6:

                            st.markdown(
                                f"**Mapping Strength**  \n"
                                f"{m.get('mapping_strength', 'Weak')}"
                            )

                        st.markdown("---")

                # =============================================
                # NO MAPPINGS
                # =============================================
                else:

                    st.warning(
                        "No semantic BSI ↔ NIST "
                        "relationship found for "
                        "this retrieved requirement."
                    )
# =====================================================
# TAB 3 — MULTI LLM COMPARISON
# =====================================================
if page == "🧠 Multi-LLM Comparison" :

    st.header("🧠 Multi-LLM Security Analysis")

    st.markdown("""
Compare OT cybersecurity responses generated by:

- Claude Sonnet 4-6
- Mistral
- Gemini-3.1-flash-lite
- GPT-5.4-nano
""")

    if "rag_results" not in st.session_state:

        st.info(
            "Please run a query first from the OT Security Assistant tab."
        )

    else:

        compare_query = st.session_state[
            "rag_results"
        ]["query"]

        st.subheader(
            "📌 Query from OT Security Assistant"
        )

        st.code(compare_query)

        if st.button("Compare Models"):

            with st.spinner(
                "Generating multi-LLM responses..."
            ):

                anthropic_result = rag(
                    query=compare_query,
                    model_name="claude-sonnet-4.6",
                    k=k
                )

                mistral_result = rag(
                    query=compare_query,
                    model_name="Mistral",
                    k=k
                )

                gemini_result = rag(
                    query=compare_query,
                    model_name="gemini-3.1-flash-lite",
                    k=k
                )

                gpt_5_result = rag(
                    query=compare_query,
                    model_name="gpt-5.4-nano",
                    k=k
                )

            col1, col2 = st.columns(2)

            with col1:

                st.subheader(
                    "Claude Sonnet 4.6"
                )

                st.write(
                    anthropic_result["answer"]
                )

            with col2:

                st.subheader("Mistral")

                st.write( mistral_result["answer"])

            col3, col4 = st.columns(2)

            with col3:

                st.subheader("Gemini-3.1-flash-lite")

                st.write(gemini_result["answer"])

            with col4:

                st.subheader("GPT-5.4-nano")

                st.write(gpt_5_result["answer"])
# =====================================================
# TAB 4 — LLM JUDGE
if page == "⚖️ LLM Judge" :

    st.header("⚖️ LLM-as-a-Judge Evaluation")

    st.markdown("""
Evaluate generated OT cybersecurity responses using:
- Relevance
- Faithfulness
- Hallucination Risk
- Technical Accuracy
- Context Utilization
- BSI ↔ NIST Semantic Validation
""")

    if "rag_results" not in st.session_state:

        st.info( "Run a query first from the OT Security Assistant tab.")

    else:

        result = st.session_state["rag_results"]

        st.subheader("📌 Query")

        st.write(result["query"])

        st.subheader("📄 Generated Answer")

        st.write( result["answer"])

        st.subheader("⚖️ Evaluation Results")

        st.write( result["evaluation_output"])
