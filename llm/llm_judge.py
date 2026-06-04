from llm.llm_router import generate_answer


# =====================================================
# COMPLETE RAG + MAPPING EVALUATION
# =====================================================
def evaluate_complete_rag(query,retrieved_context,generated_answer,results,model_name):

    # =============================================
    # BUILD MAPPING CONTEXT
    # =============================================
    mapping_context = ""

    for r in results:

        mappings = r.get(
            "mappings",
            []
        )

        for m in mappings:

            mapping_context += f"""

SOURCE STANDARD:
{r['source_standard']}

SOURCE REQUIREMENT:
{r['content']}

TARGET STANDARD:
{m['source_standard']}

TARGET REQUIREMENT:
{m['content']}

SIMILARITY SCORE:
{m['similarity_score']}

"""

    # =============================================
    # FINAL PROMPT
    # =============================================
    prompt = f"""

You are an evaluator for an
OT Cybersecurity RAG Platform.

Evaluate BOTH:

1. Generated Answer Quality
2. BSI ↔ NIST Semantic Mapping Quality

==================================================

USER QUERY:
{query}

==================================================

RETRIEVED CONTEXT:
{retrieved_context}

==================================================

GENERATED ANSWER:
{generated_answer}

==================================================

BSI ↔ NIST MAPPINGS:
{mapping_context}

==================================================

# ANSWER QUALITY

1. Relevance
- Does the answer address the user's query?

Score Guide:
1 = Not relevant
2 = Slightly relevant
3 = Partially relevant
4 = Mostly relevant
5 = Fully relevant

--------------------------------------------------

2. Faithfulness
- Is the answer supported by the retrieved context?

Score Guide:
1 = Not supported
2 = Weakly supported
3 = Partially supported
4 = Mostly supported
5 = Fully supported

--------------------------------------------------

3. Hallucination Risk
- Does the answer contain information that is NOT supported by the retrieved context?

IMPORTANT:
Lower score is BETTER.

Score Guide:
1 = No hallucination detected
2 = Very low hallucination risk
3 = Moderate hallucination risk
4 = High hallucination risk
5 = Severe hallucination risk

Consistency Rules:

- If Faithfulness = 5 then Hallucination Risk should normally be 1.
- If Faithfulness >= 4 then Hallucination Risk should not exceed 2.
- If Hallucination Risk >= 4 then Faithfulness cannot exceed 2.
- Technically correct information may still be hallucinated if it is not supported by the retrieved context.

--------------------------------------------------

4. Technical Accuracy
- Is the OT / ICS cybersecurity information technically correct?

Score Guide:
1 = Incorrect
2 = Mostly incorrect
3 = Partially correct
4 = Mostly correct
5 = Technically accurate

--------------------------------------------------

5. Context Utilization
- Did the answer effectively use the retrieved requirements?

Score Guide:
1 = No use of context
2 = Minimal use
3 = Partial use
4 = Good use
5 = Excellent use

==================================================

# MAPPING QUALITY

6. Semantic Similarity Validation
- Are the mapped BSI and NIST requirements genuinely related?

Score Guide:
1 = Unrelated
2 = Weak relationship
3 = Moderate relationship
4 = Strong relationship
5 = Highly related

--------------------------------------------------

7. Similarity Score Justification
- Is the reported similarity score reasonable?

Score Guide:
1 = Completely unreasonable
2 = Weak justification
3 = Acceptable
4 = Reasonable
5 = Fully justified

--------------------------------------------------

8. Security Objective Alignment
- Do both requirements address similar OT security objectives?

Score Guide:
1 = No alignment
2 = Weak alignment
3 = Partial alignment
4 = Good alignment
5 = Strong alignment

--------------------------------------------------

9. Lifecycle Alignment
- Are lifecycle phases reasonably aligned?

Score Guide:
1 = Not aligned
2 = Weakly aligned
3 = Partially aligned
4 = Mostly aligned
5 = Fully aligned

--------------------------------------------------

10. False Positive Risk
- Could the mapping be incorrect?

IMPORTANT:
Lower score is BETTER.

Score Guide:
1 = Very low false positive risk
2 = Low false positive risk
3 = Moderate risk
4 = High risk
5 = Very high risk

==================================================

Use this exact format:

# Answer Evaluation

Relevance: X/5
Reason: ...

Faithfulness: X/5
Reason: ...

Hallucination Risk: X/5
Reason: ...

Technical Accuracy: X/5
Reason: ...

Context Utilization: X/5
Reason: ...

==================================================

# Mapping Evaluation

Semantic Similarity Validation: X/5
Reason: ...

Similarity Score Justification: X/5
Reason: ...

Security Objective Alignment: X/5
Reason: ...

Lifecycle Alignment: X/5
Reason: ...

False Positive Risk: X/5
Reason: ...

==================================================

# Final Verdict

Overall Assessment:
...

Strengths:
...

Weaknesses:
...

"""

    # =============================================
    # GENERATE
    # =============================================
    response = generate_answer(

        model_name,

        prompt

    )

    return response