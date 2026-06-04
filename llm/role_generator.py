from llm.llm_router import generate_answer

# =====================================================
# ROLE GENERATION
# =====================================================
def generate_role(query, results, model_name):

    # =====================================
    # BUILD CONTEXT
    # =====================================
    context = ""

    for r in results:

        context += f"""
                    Title:{r['title']}
                    Content:{r['content']}
                    Lifecycle Phase:{r.get('lifecycle_phase')}
                    Normative Type:{r.get('normative_type')}
                    Source Standard:{r.get('source_standard')}

                    """
    # =====================================
    # PROMPT
    # =====================================
    prompt = f"""

            You are an OT cybersecurity expert.

            The user asked the following OT cybersecurity question:

            {query}

            Using the retrieved OT security requirements,
            determine ONLY the most relevant
            industrial and cybersecurity roles
            directly associated with this query.

            Retrieved Requirements:

            {context}

            Generate:

            1. Relevant cybersecurity or industrial roles

            2. Why these roles are responsible

            3. Operational responsibilities

            4. OT / ICS security objectives fulfilled

            5. Industrial operational impact

            Possible roles include:

            - OT Engineer
            - ICS Security Engineer
            - SCADA Administrator
            - Security Architect
            - SOC Analyst
            - Compliance Officer
            - Network Engineer
            - Plant Operator
            - Incident Responder
            - Risk Manager

            Rules:

            - Use only the retrieved requirements
            - Do not hallucinate
            - Focus specifically on the user's query
            - Only include strongly relevant roles
            - Avoid generic OT explanations
            - Be concise and technical
            - Focus on OT / ICS cybersecurity

            """

    # =====================================
    # GENERATE
    # =====================================
    response = generate_answer(prompt = prompt, model_name=model_name)

    return response


# =====================================================
# USECASE GENERATION
# =====================================================
def usecase_generation( query, results, model_name):

    # =====================================
    # BUILD CONTEXT
    # =====================================
    context = ""

    for r in results:

        context += f"""

                    Title:{r['title']}
                    Content:{r['content']}
                    Lifecycle Phase:{r.get('lifecycle_phase')}
                    Normative Type:{r.get('normative_type')}
                    Source Standard:{r.get('source_standard')}

                    """
    # =====================================
    # PROMPT
    # =====================================
    prompt = f"""

                You are an OT cybersecurity expert.

                The user asked the following OT cybersecurity question:

                {query}

                Using the retrieved OT security requirements,
                generate industrial OT/ICS use cases
                specifically related to this query.

                Retrieved Requirements:

                {context}

                Generate:

                1. Industrial OT / ICS use cases

                2. Real-world operational scenarios

                3. Security objectives fulfilled

                4. Practical implementation examples

                5. Critical OT infrastructure relevance

                Focus on:

                - SCADA
                - PLCs
                - DCS
                - Industrial Networks
                - ICS Monitoring
                - OT Authentication
                - Backup & Recovery
                - Network Segmentation
                - Endpoint hardening
                - Vulnerability and patch management
                - Security awareness for OT staff
                - Remote access management

                Rules:

                - Use only the retrieved requirements
                - Do not hallucinate
                - Focus specifically on the user's query
                - Use realistic industrial examples
                - Avoid generic cybersecurity explanations
                - Be concise and technical
                - Focus on OT / ICS cybersecurity

                """

    # =====================================
    # GENERATE
    # =====================================
    response = generate_answer( prompt = prompt, model_name=model_name)

    return response