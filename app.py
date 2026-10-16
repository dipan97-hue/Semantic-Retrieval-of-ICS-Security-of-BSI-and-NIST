import streamlit as st
import pandas as pd
import os
import warnings
import logging
import re
import markdown

from rag.rag_pipeline import rag
from llm.role_generator import generate_role, usecase_generation
from config.hitl_config import HITL_CONFIG


# ============================================================
# SUPPRESS WARNINGS
# ============================================================

warnings.filterwarnings("ignore")

warnings.simplefilter(
    action="ignore",
    category=FutureWarning
)

warnings.simplefilter(
    action="ignore",
    category=UserWarning
)


# ============================================================
# TRANSFORMERS WARNINGS
# ============================================================

logging.getLogger(
    "transformers"
).setLevel(logging.ERROR)

logging.getLogger(
    "sentence_transformers"
).setLevel(logging.ERROR)

logging.getLogger(
    "huggingface_hub"
).setLevel(logging.ERROR)


# ============================================================
# HIDE HF / TORCH WARNINGS
# ============================================================

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

os.environ["TRANSFORMERS_VERBOSITY"] = "error"

os.environ["TOKENIZERS_PARALLELISM"] = "false"

os.environ["PYTHONWARNINGS"] = "ignore"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="OT Security RAG Platform",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "current_page" not in st.session_state:

    st.session_state["current_page"] = (
        "OT Security Assistant"
    )


# ============================================================
# MAIN TITLE
# ============================================================

st.title(
    "Intelligent OT Security & Governance "
    "Requirements Analysis Platform"
)

st.markdown(
    """
AI-powered Retrieval-Augmented Generation (RAG) platform for:

- NIST SP 800-82: Cybersecurity for Industrial Control Systems
- BSI IT-Grundschutz: Basic Security Measures for Information Technology
- Semantic Requirement Mapping
- Multi-LLM Security Analysis
"""
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Settings")


# ------------------------------------------------------------
# NORMAL MODEL SELECTION
# ------------------------------------------------------------

model_name = st.sidebar.selectbox(
    "Select LLM",
    [
        "gemini-3.1-flash-lite",
        "gpt-5.4-nano",
        "claude-haiku-4-5"
    ]
)


# ------------------------------------------------------------
# NORMAL TOP-K SELECTION
# ------------------------------------------------------------

k = st.sidebar.radio(
    "Top-K Retrieval",
    options=[10, 20, 30],
    index=1
)


st.sidebar.markdown("---")


# ============================================================
# NAVIGATION
# ============================================================

PAGE_OPTIONS = [
    
    "📋 Google Form Information",

    "🧑‍🔬 HITL Evaluation",

    "🧠 Multi-LLM Comparison",

    "🤖 OT Security Assistant",

    "🔗 Knowledge Base",

    "👤 Generate Roles",

    "📊 Generate Use Cases"
   

]


# Determine currently selected page

current_page = st.session_state["current_page"]

if current_page not in PAGE_OPTIONS:

    current_page = PAGE_OPTIONS[0]

    st.session_state["current_page"] = current_page


page = st.sidebar.radio(
    "Navigation:",
    PAGE_OPTIONS,
    index=PAGE_OPTIONS.index(current_page)
)


# If user manually changes page

if page != st.session_state["current_page"]:

    st.session_state["current_page"] = page


# ============================================================
# GOOGLE FORMS
# ============================================================

st.sidebar.markdown("---")

st.sidebar.link_button(
    "📝  Evaluator A",
    "https://forms.gle/5AfLMcXA9zaKNUP79"
)

st.sidebar.link_button(
    "📝  Evaluator B",
    "https://forms.gle/W9t1gwDUxayH2GhUA"
)

st.sidebar.link_button(
    "📝  Evaluator C",
    "https://forms.gle/LV1YeYeB6e8ckmKR9"
)

st.sidebar.link_button(
    "📝  Evaluator D",
    "https://forms.gle/GJdWvgrU4jft54xj7"
)


# ============================================================
# CLEAR SESSION
# ============================================================
st.sidebar.markdown("---")

if st.sidebar.button(
    "Clear Session",
    use_container_width=True
):

    for key in list(
        st.session_state.keys()
    ):

        del st.session_state[key]

    st.rerun()


# ============================================================
# ============================================================
# PAGE 1 â€” OT SECURITY ASSISTANT
# ============================================================
# ============================================================

if page == "🤖 OT Security Assistant":

    st.header(
        "OT Security Requirements Assistant"
    )


    st.markdown(
        """
Ask cybersecurity questions related to:

- PLC Security
- Authentication
- Backup & Recovery
- Access Control
- ICS / SCADA
- Network Segmentation
- Monitoring
- OT Security Controls
- Governance
"""
    )


    # ========================================================
    # QUERY INPUT
    # ========================================================

    query = st.text_area(
        "Enter your query",
        height=150
    )


    # ========================================================
    # RUN ANALYSIS
    # ========================================================

    if st.button(
        "Run Analysis"
    ):

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
                    k=k,
                    run_judge=False
                )


            st.session_state[
                "rag_results"
            ] = result


            st.session_state[
                "rag_query"
            ] = query


            st.session_state[
                "rag_k"
            ] = k


    # ========================================================
    # SHOW GENERATED ANSWER
    # ========================================================

    if "rag_results" in st.session_state:

        result = st.session_state[
            "rag_results"
        ]


        st.subheader(
            "Generated Security Analysis"
        )


        st.markdown(
            result.get(
                "answer",
                "No answer generated."
            )
        )


# ============================================================
# ============================================================
# PAGE 2 â€” GENERATE ROLES
# ============================================================
# ============================================================

elif page == "👤 Generate Roles":

    if "rag_results" not in st.session_state:

        st.info(
            "Run a query first from the OT Security Assistant page."
        )

    else:

        query = st.session_state[
            "rag_results"
        ].get(
            "query",
            ""
        )


        st.subheader(
            "🧠 AI-Powered Operational Insights"
        )


        st.markdown(
            """
Generate OT cybersecurity roles,
industrial use cases, and operational
interpretations from retrieved requirements.
"""
        )


        # ====================================================
        # GENERATE ROLE
        # ====================================================

        if st.button(
            "Generate Role Analysis"
        ):

            with st.spinner(
                "Generating role analysis..."
            ):

                role_output = generate_role(
                    query=query,
                    results=st.session_state[
                        "rag_results"
                    ]["results"],
                    model_name=model_name
                )


                st.session_state[
                    "role_output"
                ] = role_output


        # ====================================================
        # DISPLAY ROLE
        # ====================================================

        if "role_output" in st.session_state:

            st.write(
                st.session_state[
                    "role_output"
                ]
            )


# ============================================================
# ============================================================
# PAGE 3 â€” USE CASE GENERATION
# ============================================================
# ============================================================

elif page == "📊 Generate Use Cases":

    st.header(
        "Generate Use Cases"
    )


    if "rag_results" not in st.session_state:

        st.info(
            "Run a query first from the OT Security Assistant page."
        )

    else:

        query = st.session_state[
            "rag_results"
        ].get(
            "query",
            ""
        )


        # ====================================================
        # GENERATE USE CASES
        # ====================================================

        if st.button(
            "Generate Use Cases"
        ):

            with st.spinner(
                "Generating use cases..."
            ):

                usecase_output = usecase_generation(
                    query=query,
                    results=st.session_state[
                        "rag_results"
                    ]["results"],
                    model_name=model_name
                )


                st.session_state[
                    "usecase_output"
                ] = usecase_output


        # ====================================================
        # DISPLAY USE CASES
        # ====================================================

        if "usecase_output" in st.session_state:

            st.write(
                st.session_state[
                    "usecase_output"
                ]
            )


# ============================================================
# ============================================================
# PAGE 4 — KNOWLEDGE BASE
# ============================================================
# ============================================================

elif page == "🔗 Knowledge Base":

    st.header(
        "Knowledge Base"
    )


    st.markdown(
        """
Explore retrieved OT cybersecurity
requirements, their originating standards,
and semantic relationships between
BSI and NIST.
"""
    )


    # ========================================================
    # CHECK RESULTS
    # ========================================================

    if "rag_results" not in st.session_state:

        st.info(
            "Run a query first from the OT Security Assistant tab."
        )

    else:

        result = st.session_state[
            "rag_results"
        ]


        # ====================================================
        # RETRIEVED RESULTS
        # ====================================================

        for idx, r in enumerate(
            result.get(
                "results",
                []
            )
        ):

            mappings = r.get(
                "mappings",
                []
            )


            # =================================================
            # EXPANDER
            # =================================================

            with st.expander(
                f"{idx + 1}. "
                f"{r.get('title', 'Requirement')}"
            ):


                # =============================================
                # PRIMARY REQUIREMENT
                # =============================================

                st.markdown(
                    f"## ðŸ“„ "
                    f"{r.get('source_standard', 'Unknown')}"
                )


                st.markdown(
                    "### Extracted Requirement"
                )


                st.write(
                    r.get(
                        "content",
                        ""
                    )
                )


                st.markdown("---")


                # =============================================
                # PRIMARY METADATA
                # =============================================

                col1, col2, col3 = st.columns(3)


                # ---------------------------------------------
                # LIFECYCLE
                # ---------------------------------------------

                with col1:

                    st.markdown(
                        f"**Lifecycle Phase**  \n"
                        f"{r.get('lifecycle_phase', 'None')}"
                    )


                # ---------------------------------------------
                # NORMATIVE
                # ---------------------------------------------

                with col2:

                    st.markdown(
                        f"**Normative Type**  \n"
                        f"{r.get('normative_type', 'None')}"
                    )


                # ---------------------------------------------
                # SIMILARITY
                # ---------------------------------------------

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
                        f"**BSI and NIST Similarity**  \n"
                        f"{similarity}"
                    )


                # =============================================
                # RELATED REQUIREMENTS
                # =============================================

                st.markdown("---")

                st.markdown(
                    "## Related Requirement"
                )


                # =============================================
                # MAPPINGS EXIST
                # =============================================

                if mappings:

                    for m in mappings:

                        similarity = round(
                            m.get(
                                "similarity_score",
                                0
                            ),
                            3
                        )


                        # -------------------------------------
                        # RELATED STANDARD
                        # -------------------------------------

                        st.success(
                            f"{m.get('source_standard', 'Unknown')} "
                            f"relationship found "
                            f"(Similarity: {similarity})"
                        )


                        # -------------------------------------
                        # RELATED TITLE
                        # -------------------------------------

                        st.markdown(
                            f"### {m.get('title', 'Related Requirement')}"
                        )


                        # -------------------------------------
                        # RELATED CONTENT
                        # -------------------------------------

                        st.write(
                            m.get(
                                "content",
                                ""
                            )
                        )


                        # -------------------------------------
                        # RELATED METADATA
                        # -------------------------------------

                        col4, col5, col6 = st.columns(3)


                        with col4:

                            st.markdown(
                                f"**Lifecycle**  \n"
                                f"{m.get('lifecycle_phase', 'None')}"
                            )


                        with col5:

                            st.markdown(
                                f"**Normative**  \n"
                                f"{m.get('normative_type', 'None')}"
                            )


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
                        "No semantic BSI and NIST "
                        "relationship found for "
                        "this retrieved requirement."
                    )


# ============================================================
# ============================================================
# PAGE 5 - HITL EVALUATION
# ============================================================
# ============================================================

elif page == "🧑‍🔬 HITL Evaluation":

    st.header(
        "🧑‍🔬 Human-in-the-Loop (HITL) Evaluation"
    )


    st.write(
        "Select an evaluator to view the four "
        "assigned OT cybersecurity queries."
    )


    # ========================================================
    # SELECT EVALUATOR
    # ========================================================

    evaluator = st.selectbox(
        "Select Evaluator",
        list(
            HITL_CONFIG.keys()
        )
    )


    assigned_queries = HITL_CONFIG[
        evaluator
    ]


    # ========================================================
    # EVALUATOR INFORMATION
    # ========================================================

    st.info(
        f"{evaluator} has been assigned "
        f"{len(assigned_queries)} predefined queries."
    )


    # ========================================================
    # ASSIGNED QUERIES
    # ========================================================

    st.subheader(
        "Assigned Queries"
    )


    query_labels = [

        f"{item['query_id']} - {item['category']}"

        for item in assigned_queries
    ]


    selected_label = st.selectbox(
        "Select a query",
        query_labels
    )


    selected_index = query_labels.index(
        selected_label
    )


    selected = assigned_queries[
        selected_index
    ]


    # ========================================================
    # QUERY INFORMATION
    # ========================================================

    st.divider()


    st.subheader(
        f"{selected['query_id']} "
        f"{selected['category']}"
    )


    st.write(
        selected["query"]
    )


    # ========================================================
    # FIXED MODEL + TOP-K
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            "# Assigned Model"
        )

        st.info(
            selected["model"]
        )


    with col2:

        st.markdown(
            "##### Top-K"
        )

        st.info(
            str(
                selected["top_k"]
            )
        )


    st.caption(
        "The model and Top-K value are predefined "
        "for this query and cannot be changed by "
        "the evaluator."
    )


    # ========================================================
    # GENERATE SINGLE HITL ANSWER
    # ========================================================

    if st.button(
        "🧠 Generate Answer",
        use_container_width=True
    ):

        with st.spinner(
            "Generating OT cybersecurity response..."
        ):

            result = rag(
                query=selected["query"],
                model_name=selected["model"],
                k=selected["top_k"],
                run_judge=False
            )


        # ====================================================
        # SAVE RESULT
        # ====================================================

        st.session_state[
            "hitl_result"
        ] = result


        st.session_state[
            "hitl_query_id"
        ] = selected[
            "query_id"
        ]


        st.session_state[
            "hitl_category"
        ] = selected[
            "category"
        ]


        st.session_state[
            "hitl_query"
        ] = selected[
            "query"
        ]


        st.session_state[
            "hitl_model"
        ] = selected[
            "model"
        ]


        st.session_state[
            "hitl_k"
        ] = selected[
            "top_k"
        ]


        st.session_state[
            "hitl_evaluator"
        ] = evaluator


        st.success(
            "Answer generated successfully."
        )


    # ========================================================
    # DISPLAY HITL RESULT
    # ========================================================

    if "hitl_result" in st.session_state:

        result = st.session_state[
            "hitl_result"
        ]


        # ====================================================
        # ONLY DISPLAY RESULT FOR CURRENT QUERY
        # ====================================================

        if (
            st.session_state.get(
                "hitl_query_id"
            )
            == selected["query_id"]
        ):


            st.divider()


            st.subheader(
                f"🤖 {selected['query_id']} — "
                f"Generated Analysis"
            )


            # =================================================
            # RESULT TABS
            # =================================================

            answer_tab, context_tab = st.tabs(
                [
                    "🤖 Generated Response",
                    "📚 Retrieved Context"
                ]
            )


            # =================================================
            # GENERATED RESPONSE
            # =================================================

            with answer_tab:

                st.markdown(
                    result.get(
                        "answer",
                        "No answer generated."
                    )
                )


            # =========================================================
            # RETRIEVED KNOWLEDGE BASE
            # =========================================================

            with context_tab:

                st.subheader(
                    "📚 Retrieved Knowledge Base"
                )

                st.caption(
                    f"Query: {selected['query_id']} | "
                    f"Top-K: {selected['top_k']}"
                )

                retrieved_results = result.get(
                    "results",
                    []
                )

                if not retrieved_results:

                    st.info(
                        "No retrieved requirements available."
                    )

                else:

                    # =================================================
                    # LOOP THROUGH RETRIEVED REQUIREMENTS
                    # =================================================

                    for idx, r in enumerate(
                        retrieved_results
                    ):

                        mappings = r.get(
                            "mappings",
                            []
                        )

                        title = r.get(
                            "title",
                            f"Requirement {idx + 1}"
                        )

                        # =============================================
                        # REQUIREMENT EXPANDER
                        # =============================================

                        with st.expander(
                            f"{idx + 1}. {title}",
                            expanded=False
                        ):

                            # =========================================
                            # PRIMARY REQUIREMENT
                            # =========================================

                            st.markdown(
                                f"## 📄 "
                                f"{r.get('source_standard', 'Unknown')}"
                            )

                            st.markdown(
                                "### Extracted Requirement"
                            )

                            st.write(
                                r.get(
                                    "content",
                                    ""
                                )
                            )

                            st.markdown("---")

                            # =========================================
                            # METADATA
                            # =========================================

                            col1, col2, col3 = st.columns(3)

                            # -----------------------------------------
                            # LIFECYCLE
                            # -----------------------------------------

                            with col1:

                                st.markdown(
                                    "**Lifecycle Phase**"
                                )

                                st.write(
                                    r.get(
                                        "lifecycle_phase",
                                        "None"
                                    )
                                )

                            # -----------------------------------------
                            # NORMATIVE TYPE
                            # -----------------------------------------

                            with col2:

                                st.markdown(
                                    "**Normative Type**"
                                )

                                st.write(
                                    r.get(
                                        "normative_type",
                                        "None"
                                    )
                                )

                            # -----------------------------------------
                            # BSI â†” NIST SIMILARITY
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
                                    "**BSI-NIST Similarity**"
                                )

                                st.write(
                                    similarity
                                )

                            # =========================================
                            # RELATED REQUIREMENTS
                            # =========================================

                            st.markdown("---")

                            st.markdown(
                                "## Related Requirement"
                            )

                            if mappings:

                                for m in mappings:

                                    similarity = round(
                                        m.get(
                                            "similarity_score",
                                            0
                                        ),
                                        3
                                    )

                                    # ---------------------------------
                                    # RELATIONSHIP
                                    # ---------------------------------

                                    st.success(
                                        f"{m.get('source_standard', 'Unknown')} "
                                        f"relationship found "
                                        f"(Similarity: {similarity})"
                                    )

                                    # ---------------------------------
                                    # RELATED TITLE
                                    # ---------------------------------

                                    st.markdown(
                                        f"### {m.get('title', 'Related Requirement')}"
                                    )

                                    # ---------------------------------
                                    # RELATED CONTENT
                                    # ---------------------------------

                                    st.write(
                                        m.get(
                                            "content",
                                            ""
                                        )
                                    )

                                    # ---------------------------------
                                    # RELATED METADATA
                                    # ---------------------------------

                                    col4, col5, col6 = st.columns(3)

                                    with col4:

                                        st.markdown(
                                            "**Lifecycle Phase**"
                                        )

                                        st.write(
                                            m.get(
                                                "lifecycle_phase",
                                                "None"
                                            )
                                        )

                                    with col5:

                                        st.markdown(
                                            "**Normative Type**"
                                        )

                                        st.write(
                                            m.get(
                                                "normative_type",
                                                "None"
                                            )
                                        )

                                    with col6:

                                        st.markdown(
                                            "**Mapping Strength**"
                                        )

                                        st.write(
                                            m.get(
                                                "mapping_strength",
                                                "Weak"
                                            )
                                        )

                                    st.markdown("---")

                            else:

                                st.warning( "No semantic BSI-NIST "
                                    "relationship found for "
                                    "this retrieved requirement."
                                )


                        # =================================================
            # MULTI-LLM COMPARISON
            # =================================================

            st.divider()


            st.subheader(
                "🧠 Multi-LLM Comparison"
            )


            st.write(
                "Compare this query across all three "
                "LLMs using the same Top-K value."
            )


            st.info(
                f"Query: {selected['query_id']} | "
                f"Top-K: {selected['top_k']}"
            )


            if st.button(
                "Open Multi-LLM Comparison",
                use_container_width=True
            ):

                # =============================================
                # PASS HITL QUERY TO MULTI-LLM
                # =============================================

                st.session_state[
                    "multi_llm_from_hitl"
                ] = True


                st.session_state[
                    "multi_llm_query_id"
                ] = selected[
                    "query_id"
                ]


                st.session_state[
                    "multi_llm_category"
                ] = selected[
                    "category"
                ]


                st.session_state[
                    "multi_llm_query"
                ] = selected[
                    "query"
                ]


                st.session_state[
                    "multi_llm_k"
                ] = selected[
                    "top_k"
                ]


                st.session_state[
                    "multi_llm_evaluator"
                ] = evaluator


                # =============================================
                # MOVE TO MULTI-LLM PAGE
                # =============================================

                st.session_state[
                    "current_page"
                ] = "🧠 Multi-LLM Comparison"


                st.rerun()


# ============================================================
# ============================================================
# PAGE 6 â€” MULTI-LLM COMPARISON
# ============================================================
# ============================================================

if page == "🧠 Multi-LLM Comparison":

    st.header(
        "🧠 Multi-LLM Security Analysis"
    )


    # ========================================================
    # MODELS
    # ========================================================

    MULTI_LLM_MODELS = [

        (
            "GPT-5.4-nano",
            "gpt-5.4-nano"
        ),

        (
            "Gemini 3.1 Flash Lite",
            "gemini-3.1-flash-lite"
        ),


        (
            "Claude Haiku 4.5",
            "claude-haiku-4-5"
        )
    ]


    # ========================================================
    # CHECK HITL MODE
    # ========================================================

    from_hitl = st.session_state.get(
        "multi_llm_from_hitl",
        False
    )


    if from_hitl:

        # ====================================================
        # GET HITL QUERY
        # ====================================================

        compare_query = st.session_state[
            "multi_llm_query"
        ]


        compare_k = st.session_state[
            "multi_llm_k"
        ]


        query_id = st.session_state[
            "multi_llm_query_id"
        ]


        category = st.session_state[
            "multi_llm_category"
        ]


        evaluator = st.session_state.get(
            "multi_llm_evaluator",
            ""
        )


        # ====================================================
        # DISPLAY HITL INFORMATION
        # ====================================================

        st.success(
            f"HITL Query: {query_id} | "
            f"Category: {category} | "
            f"Evaluator: {evaluator} | "
            f"Top-K: {compare_k}"
        )


        st.subheader(
            f"{query_id} — {category}"
        )


        st.write(
            compare_query
        )


        st.info(
            f"Top-K is fixed to {compare_k}. "
            "All three models will use this same Top-K value."
        )


    else:

        # ====================================================
        # NORMAL MULTI-LLM MODE
        # ====================================================

        if "rag_results" not in st.session_state:

            st.info(
                "Please run a query first from "
                "the OT Security Assistant tab."
            )

            compare_query = ""

        else:

            compare_query = st.session_state[
                "rag_results"
            ].get(
                "query",
                ""
            )


        st.subheader(
            "🤖 Query"
        )


        st.info(
            compare_query
        )


        compare_k = k


    # ========================================================
    # GENERATE THREE MODELS
    # ========================================================

    if compare_query:

        if st.button(
            "🧠 Compare Models",
            use_container_width=True
        ):

            multi_results = {}


            with st.spinner(
                "Generating responses from all three models..."
            ):

                for display_name, model in MULTI_LLM_MODELS:

                    result = rag(
                        query=compare_query,
                        model_name=model,
                        k=compare_k,
                        run_judge=False
                    )


                    multi_results[
                        display_name
                    ] = result


            # =================================================
            # SAVE RESULTS
            # =================================================

            st.session_state[
                "comparison_results"
            ] = multi_results


            st.session_state[
                "comparison_query"
            ] = compare_query


            st.session_state[
                "comparison_k"
            ] = compare_k


            if from_hitl:

                st.session_state[
                    "comparison_query_id"
                ] = query_id


                st.session_state[
                    "comparison_category"
                ] = category


    # ========================================================
    # DISPLAY RESULTS
    # ========================================================

    if "comparison_results" in st.session_state:

        results = st.session_state[
            "comparison_results"
        ]


        st.divider()


        st.subheader(
            "🧠 Multi-LLM Comparison"
        )


        if "comparison_query_id" in st.session_state:

            st.info(
                f"Query: "
                f"{st.session_state['comparison_query_id']} | "
                f"Top-K: "
                f"{st.session_state['comparison_k']}"
            )

        else:

            st.info(
                f"Top-K: "
                f"{st.session_state['comparison_k']}"
            )


        # ====================================================
        # CLEAN ANSWER
        # ====================================================

        def clean_answer(result):

            if isinstance(
                result,
                dict
            ):

                text = result.get(
                    "answer",
                    ""
                )

            else:

                text = result


            if not text:

                return "No response generated."


            text = str(
                text
            ).strip()


            # ------------------------------------------------
            # Remove first markdown title
            # ------------------------------------------------

            lines = text.splitlines()


            if (
                lines
                and re.match(
                    r"^\s*#{1,6}\s+",
                    lines[0]
                )
            ):

                lines = lines[1:]


            text = "\n".join(
                lines
            )


            # ------------------------------------------------
            # Convert single asterisk bullets
            # ------------------------------------------------

            text = re.sub(
                r"(?<!\*)\*\s+",
                "\n- ",
                text
            )


            # ------------------------------------------------
            # Remove horizontal separators
            # ------------------------------------------------

            text = re.sub(
                r"^\s*---+\s*$",
                "",
                text,
                flags=re.MULTILINE
            )


            # ------------------------------------------------
            # Remove accidental HTML
            # ------------------------------------------------

            text = re.sub(
                r"<(?!https?://)[^>]*>",
                "",
                text
            )


            # ------------------------------------------------
            # Numbered section headers
            # ------------------------------------------------

            text = re.sub(
                r"\n?(\d+\.\s+[^:\n]{1,80}:)",
                r"\n\n**\1**\n",
                text
            )


            # ------------------------------------------------
            # Bullet sub-labels
            # ------------------------------------------------

            text = re.sub(
                r"^-\s+([^:\n]{1,80}):",
                r"- **\1:**",
                text,
                flags=re.MULTILINE
            )


            # ------------------------------------------------
            # Collapse excessive blank lines
            # ------------------------------------------------

            text = re.sub(
                r"\n{3,}",
                "\n\n",
                text
            )


            return text.strip()


        # ====================================================
        # FORMAT MARKDOWN
        # ====================================================

        def format_answer(text):

            return markdown.markdown(
                text,
                extensions=[
                    "extra",
                    "sane_lists"
                ]
            )


        # ====================================================
        # PREPARE ANSWERS
        # ====================================================

        answer_html = {}


        for display_name, model in MULTI_LLM_MODELS:

            clean = clean_answer(
                results.get(
                    display_name,
                    {}
                )
            )


            answer_html[
                display_name
            ] = format_answer(
                clean
            )


        # ====================================================
        # FOUR-COLUMN HTML TABLE
        # ====================================================

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
            font-size: 17px;
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
                        Claude Haiku 4.5
                    </th>

                </tr>

            </thead>


            <tbody>

                <tr>

                    <td>
                        {answer_html["GPT-5.4-nano"]}
                    </td>

                    <td>
                        {answer_html["Gemini 3.1 Flash Lite"]}
                    </td>


                    <td>
                        {answer_html["Claude Haiku 4.5"]}
                    </td>

                </tr>

            </tbody>

        </table>
        """


        st.html(
            table_html
        )


# ============================================================
# ============================================================
# PAGE 7  GOOGLE FORM INFORMATION
# ============================================================
# ============================================================

if page == "📋 Google Form Information":

    st.header(
        " Human Evaluation Information"
    )


    st.markdown(
        """
This evaluation is part of a Master's thesis
investigating an AI-powered OT Security Assistant
developed for OT cybersecurity requirement analysis
using NIST SP 800-82 and BSI IT-Grundschutz.

Each evaluator will receive four predefined queries.
The Model and Top-K value are automatically configured
for each query.
"""
    )


    st.markdown("---")


    # ========================================================
    # EVALUATION PROCEDURE
    # ========================================================

    st.subheader(
        "Evaluation Procedure"
    )


    st.markdown(
        """
### Step 1

Open the **HITL Evaluation** page.

### Step 2

Select your assigned evaluator.

### Step 3

Select one of the four assigned queries.

### Step 4

The assigned Model and Top-K value will be shown automatically.

### Step 5

Click **Generate Answer**.

### Step 6

Read the generated response carefully.

### Step 7

Open the **Retrieved Context** tab and review the knowledge retrieved from the BSI and NIST knowledge base.

### Step 8

If required, click **Multi-LLM Comparison** to compare the same query using the same Top-K value across the available LLMs.

### Step 9

Evaluate the generated information using the assigned Google Form.

### Step 10

Repeat the process for your remaining assigned queries.
"""
    )


    st.markdown("---")


    # ========================================================
    # WHAT TO EVALUATE
    # ========================================================

    st.subheader(
        "What should you evaluate?"
    )


    st.markdown(
        """
Please evaluate:

- Is the generated answer relevant to the query?
- Is the generated answer understandable?
- Is the technical information accurate and trustworthy?
- Is the answer appropriate for an OT/ICS environment?
- Is the retrieved knowledge understandable and relevant?
- Are the BSI and NIST requirements relevant to the query?
- Is the information presented clearly?
"""
    )


    st.markdown("---")


    # ========================================================
    # IMPORTANT
    # ========================================================

    st.subheader(
        "Important Instructions"
    )


    st.info(
        """
- Use only your assigned queries.
- Do not modify or rephrase the queries.
- The Model and Top-K are predefined.
- Do not change the assigned Model or Top-K.
- Read the generated response carefully.
- Review the Retrieved Context before evaluation.
- Use the Multi-LLM Comparison when requested.
- There are no right or wrong answers.
- Provide your honest opinion.
"""
    )


    st.markdown("---")
    st.info("Note - You can try the queries in the OT Security Assistant tab with different K values " \
    "to check the authenticity of the result. Also you can try with different queries related to this domain and check and mention in the google form..")

    # ========================================================
    # COMPLETION TIME
    # ========================================================

    st.subheader(
        "Estimated Completion Time"
    )


    st.success(
        "Approximately 15-20 minutes."
    )
