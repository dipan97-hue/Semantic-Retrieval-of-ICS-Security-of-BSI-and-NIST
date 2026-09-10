def build_cross_model_judge_prompt(
    query,
    candidate_answer,
    candidate_context
):

    return f"""
You are evaluating an AI-generated answer from an
OT cybersecurity Retrieval-Augmented Generation system.

Your task is to evaluate the candidate answer strictly
using the user's query and the retrieved context.

Do NOT judge the answer based on:
- model identity
- writing style
- verbosity
- answer length
- personal preference

Focus on technical, factual, evidence-based quality.

The system is designed for OT / ICS cybersecurity.

Therefore, consider:

- safety
- availability
- reliability
- legacy systems
- deterministic operation
- operational constraints
- maintenance windows
- OT-specific cybersecurity risks

The answer should be supported by the retrieved
BSI IT-Grundschutz and/or NIST SP 800-82 context.

Do not reward unsupported claims about:
- certification
- compliance
- guaranteed security
- specific standards not present in the context

==================================================
USER QUERY
==================================================

{query}

==================================================
RETRIEVED CONTEXT
==================================================

{candidate_context}

==================================================
CANDIDATE ANSWER
==================================================

{candidate_answer}

==================================================
EVALUATION CRITERIA
==================================================

Score each criterion from 1 to 5.

1. Relevance
Does the answer directly address the user's query?

2. Technical Accuracy
Are the OT cybersecurity recommendations technically correct?

3. Faithfulness
Are the claims supported by the retrieved context?

4. Completeness
Does the answer cover the important aspects of the query?

5. OT Operational Suitability
Does the answer respect OT safety, availability,
reliability and operational constraints?

6. BSI/NIST Alignment
Is the answer consistent with the retrieved
BSI IT-Grundschutz and/or NIST SP 800-82 requirements?

7. Hallucination Risk
1 = very low hallucination risk
5 = very high hallucination risk

8. Overall Quality
1 = very poor
5 = excellent

==================================================
OUTPUT FORMAT
==================================================

Return ONLY valid JSON.

{{
    "relevance": 1,
    "technical_accuracy": 1,
    "faithfulness": 1,
    "completeness": 1,
    "ot_operational_suitability": 1,
    "bsi_nist_alignment": 1,
    "hallucination_risk": 1,
    "overall_quality": 1,
    "reason": "Brief explanation of the evaluation."
}}"""