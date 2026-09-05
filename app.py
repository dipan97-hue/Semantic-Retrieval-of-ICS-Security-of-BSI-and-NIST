import streamlit as st
import pandas as pd
import html
from rag.rag_pipeline import rag
from llm.role_generator import generate_role, usecase_generation
from llm.llm_judge import evaluate_complete_rag as evaluate_rag_response
import os
import warnings
import logging
import re
import markdown

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
        "Mistral",
        "gemini-3.1-flash-lite",
        "gpt-5.4-nano",
        "claude-haiku-4-5",

    ]
)

k = st.sidebar.radio(
    "Top-K Retrieval",
    options=[10, 20, 30],
    index=1
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
        "📋 Google Form Information"

       
    ])

st.sidebar.link_button("📝 Group A",'https://forms.gle/QALL2nKFAyt2AXgj6')
st.sidebar.link_button("📝 Group B",'https://forms.gle/TPCif4KJ5zf1Mfc1A')
st.sidebar.link_button("📝 Group C",'https://forms.gle/DZw8VSMfAWtB9AH29')
st.sidebar.link_button("📝 Group D",'https://forms.gle/a8z6Q6TGrZ8Bym3d9')
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

        st.markdown(result["answer"])

# =====================================
# # AI INSIGHTS
# =====================================
elif page == "👤 Generate Roles" :
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
    
elif page == "📊 Generate Use Cases" :
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
elif page == "🔗 Knowledge Base" :

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
elif page == "🧠 Multi-LLM Comparison":

    st.header("🧠 Multi-LLM Security Analysis")

    st.markdown(
        """
        Compare OT cybersecurity responses generated by:

        - GPT-5.4-nano
        - Gemini 3.1 Flash Lite
        - Mistral
        - Claude Haiku 4.5
        """
    )

    if "rag_results" not in st.session_state:

        st.info(
            "Please run a query first from the OT Security Assistant tab."
        )

    else:

        compare_query = st.session_state["rag_results"]["query"]

        st.subheader("📌 Query")
        st.info(compare_query)

        # ---------------------------------------------------------
        # GENERATE RESPONSES
        # ---------------------------------------------------------

        if st.button("Compare Models"):

            with st.spinner("Generating responses from all models..."):

                gpt_5_result = rag(
                    query=compare_query,
                    model_name="gpt-5.4-nano",
                    k=k
                )

                gemini_result = rag(
                    query=compare_query,
                    model_name="gemini-3.1-flash-lite",
                    k=k
                )

                mistral_result = rag(
                    query=compare_query,
                    model_name="Mistral",
                    k=k
                )

                anthropic_result = rag(
                    query=compare_query,
                    model_name="claude-haiku-4-5",
                    k=k
                )

            st.session_state["comparison_results"] = {
                "GPT-5.4-nano": gpt_5_result,
                "Gemini 3.1 Flash Lite": gemini_result,
                "Mistral": mistral_result,
                "Claude Haiku 4.5": anthropic_result
            }

        # ---------------------------------------------------------
        # DISPLAY RESULTS
        # ---------------------------------------------------------

        if "comparison_results" in st.session_state:

            results = st.session_state["comparison_results"]

            st.divider()

            st.subheader("📊 Multi-LLM Comparison")

            # -----------------------------------------------------
            # CLEAN ANSWER
            # -----------------------------------------------------

            def clean_answer(result):

                if isinstance(result, dict):
                    text = result.get("answer", "")
                else:
                    text = result

                if not text:
                    return "No response generated."

                text = str(text).strip()

                # Handle short failure messages (e.g. "Mistral generation failed.") as-is
                if len(text.split()) <= 6 and "fail" in text.lower():
                    return text

                # -------------------------------------------------
                # Remove first model-generated title line (e.g. "# User Auth in ICS")
                # -------------------------------------------------
                lines = text.splitlines()
                if lines and re.match(r"^\s*#{1,6}\s+", lines[0]):
                    lines = lines[1:]
                text = "\n".join(lines)

                # -------------------------------------------------
                # STEP 1: Convert single-asterisk bullet markers ("* Item")
                # into proper markdown list items on their own line.
                # Must run BEFORE we strip asterisks, and must not touch "**bold**".
                # -------------------------------------------------
                text = re.sub(r"(?<!\*)\*(?!\*)\s+", r"\n- ", text)

                # -------------------------------------------------
                # STEP 2: Strip all remaining asterisks (broken/inconsistent bold).
                # We rebuild our own bold formatting below instead.
                # -------------------------------------------------
                text = text.replace("*", "")

                # -------------------------------------------------
                # Remove horizontal separators
                # -------------------------------------------------
                text = re.sub(r"^\s*---+\s*$", "", text, flags=re.MULTILINE)

                # -------------------------------------------------
                # Remove accidental HTML
                # -------------------------------------------------
                text = re.sub(r"<(?!https?://)[^>]*>", "", text)

                # -------------------------------------------------
                # STEP 3: Force a blank line before every numbered section header
                # e.g. "1. Summary:" or "2. Key security controls:"
                # -------------------------------------------------
                text = re.sub(
                    r"\s*(\d+\.\s+[A-Za-z][^:\n]{0,80}:)",
                    r"\n\n\1",
                    text
                )

                # Ensure content after the header colon starts on a new line
                text = re.sub(
                    r"(\d+\.\s+[^:\n]+:)\s+(?=\S)",
                    r"\1\n",
                    text
                )

                # Bold the numbered headers
                text = re.sub(
                    r"^(\d+\.\s+[^:\n]+:)",
                    r"**\1**",
                    text,
                    flags=re.MULTILINE
                )

                # -------------------------------------------------
                # STEP 4: Bold bullet sub-labels before their colon
                # e.g. "- Physical Access Controls: Used as..." 
                #   -> "- **Physical Access Controls:** Used as..."
                # -------------------------------------------------
                text = re.sub(
                    r"^-\s+([^:\n]{1,80}):",
                    r"- **\1:**",
                    text,
                    flags=re.MULTILINE
                )

                # -------------------------------------------------
                # Collapse excess blank lines
                # -------------------------------------------------
                text = re.sub(r"\n{3,}", "\n\n", text)

                return text.strip()

            # -----------------------------------------------------
            # FORMAT MARKDOWN
            # -----------------------------------------------------

            def format_answer(text):

                return markdown.markdown(
                    text,
                    extensions=[
                        "extra",
                        "sane_lists"
                    ]
                )

            # -----------------------------------------------------
            # GET CLEAN ANSWERS
            # -----------------------------------------------------

            gpt_answer = clean_answer(
                results["GPT-5.4-nano"]
            )

            gemini_answer = clean_answer(
                results["Gemini 3.1 Flash Lite"]
            )

            mistral_answer = clean_answer(
                results["Mistral"]
            )

            claude_answer = clean_answer(
                results["Claude Haiku 4.5"]
            )

            # -----------------------------------------------------
            # CONVERT MARKDOWN → HTML
            # -----------------------------------------------------

            gpt_html = format_answer(gpt_answer)

            gemini_html = format_answer(gemini_answer)

            mistral_html = format_answer(mistral_answer)

            claude_html = format_answer(claude_answer)

            # -----------------------------------------------------
            # COMPARISON TABLE
            # -----------------------------------------------------

            table_html = f"""
            <style>

            .comparison-table {{
                width: 100%;
                border-collapse: collapse;
                table-layout: fixed;
                font-family: Arial, sans-serif;
            }}

            .comparison-table th {{
                border: 1px solid #999;
                padding: 14px;
                text-align: left;
                font-size: 18px;
                font-weight: 700;
                vertical-align: top;
                background-color: #f5f5f5;
            }}

            .comparison-table td {{
                border: 1px solid #999;
                padding: 16px;
                vertical-align: top;
                text-align: left;
                font-size: 14px;
                line-height: 1.6;
                overflow-wrap: anywhere;
                word-break: normal;
            }}

            .comparison-table th,
            .comparison-table td {{
                width: 25%;
            }}

            .comparison-table p {{
                margin-top: 0;
                margin-bottom: 14px;
            }}

            .comparison-table strong {{
                font-weight: 700;
            }}

            .comparison-table ul {{
                margin-top: 6px;
                margin-bottom: 14px;
                padding-left: 22px;
            }}

            .comparison-table ol {{
                margin-top: 6px;
                margin-bottom: 14px;
                padding-left: 22px;
            }}

            .comparison-table li {{
                margin-bottom: 7px;
            }}

            .comparison-table h1,
            .comparison-table h2,
            .comparison-table h3,
            .comparison-table h4 {{
                font-size: 16px;
                margin-top: 12px;
                margin-bottom: 8px;
            }}

            .comparison-table table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
                margin-bottom: 15px;
            }}

            .comparison-table table th {{
                font-size: 13px;
                padding: 8px;
            }}

            .comparison-table table td {{
                font-size: 13px;
                padding: 8px;
            }}

            .comparison-table hr {{
                margin: 12px 0;
            }}

            </style>

            <table class="comparison-table">

                <thead>

                    <tr>

                        <th>
                            GPT-5.4-nano
                        </th>

                        <th>
                            Gemini 3.1 Flash Lite
                        </th>

                        <th>
                            Mistral
                        </th>

                        <th>
                            Claude Haiku 4.5
                        </th>

                    </tr>

                </thead>

                <tbody>

                    <tr>

                        <td>
                            {gpt_html}
                        </td>

                        <td>
                            {gemini_html}
                        </td>

                        <td>
                            {mistral_html}
                        </td>

                        <td>
                            {claude_html}
                        </td>

                    </tr>

                </tbody>

            </table>
            """

            st.html(table_html)

elif page == "📋 Google Form Information":


    st.markdown("""

This evaluation is part of a Master's thesis investigating an AI-powered OT Security Assistant developed for OT cybersecurity requirement analysis using NIST SP 800-82 and BSI IT-Grundschutz.

Your task is to evaluate the usability, understandability, and relevance of the generated information. Each student will do 4 queries as per the group allotment.
(For example students allotted in Group A will click on Group A form and perform those 4 queries only. )

Please follow the steps below carefully.

""")

    st.markdown("---")

    st.subheader(
        "📝 Evaluation Procedure"
    )

    st.markdown("""

### Step 1

Copy and paste **one assigned query at a time** into the **OT Security Assistant** page.

### Step 2

Click **Run Analysis**.

### Step 3

Read the generated answer carefully.

### Step 4

Open the **Knowledge Base** tab and verify whether the retrieved requirements are understandable and relevant to the query. Also check
    whether the similarity scores between BSI and NIST requirements are meaningful and whether the related requirements are relevant to the query.
    

### Step 5

Open the **Generate Use Cases** tab and review the generated use cases.

### Step 6

Open the **Generate Roles** tab and review the generated OT security roles.

### Step 7

Open the **Multi-LLM Comparison** tab and compare the responses generated by different AI models and mark which model according gives the best answer.


### Step 8

Open your assigned Google Form  as per your group allotment and provide your ratings.

### Step 9

Repeat the same process for the remaining assigned queries.

### Note: You can check with Top-K retrieval values of 10, 20, and 30 to see if the generated answer changes.


""")

    st.markdown("---")

    st.subheader(
        "📌 What should you evaluate?"
    )

    st.markdown("""

Please evaluate:

- Is the generated answer understandable?

- Is the generated answer relevant to the query?

- Is the information trustworthy?

- Are the generated use cases useful?

- Are the generated OT security roles meaningful?

- Is the Knowledge Base easy to understand?

- Is the information presented clearly?

""")

    st.markdown("---")

    st.subheader(
        "⚠️ Important Instructions"
    )

    st.info("""

• Use only the assigned queries.

• Do not modify or rephrase the queries.

• Copy and paste one query at a time.

• Visit all tabs before completing the Google Form.

• There are no right or wrong answers.

• Please provide your honest opinion.

""")

    st.markdown("---")

    st.subheader(
        "⏱ Estimated Completion Time"
    )

    st.success(
        "Approximately 15 - 20 minutes."
    )