HITL_CONFIG = {

    "Evaluator A": [

        {
            "query_id": "Q01",
            "category": "PLC Security",
            "query": "How should PLCs be authenticated in OT environments?",
            "model": "claude-haiku-4-5",
            "top_k": 30
        },

        {
            "query_id": "Q04",
            "category": "Authentication",
            "query": "What authentication mechanisms are recommended for OT environments?",
            "model": "gpt-5.4-nano",
            "top_k": 10
        },

        {
            "query_id": "Q09",
            "category": "Network Segmentation",
            "query": "How should OT networks be segmented?",
            "model": "gemini-3.1-flash-lite",
            "top_k": 10
        },

        {
            "query_id": "Q14",
            "category": "OT Security Controls",
            "query": "How should vulnerability management be performed in OT?",
            "model": "gpt-5.4-nano",
            "top_k": 10
        }
    ],


    "Evaluator B": [

        {
            "query_id": "Q02",
            "category": "PLC Security",
            "query": "What security controls should be applied to PLC programming interfaces?",
            "model": "gpt-5.4-nano",
            "top_k": 20
        },

        {
            "query_id": "Q07",
            "category": "ICS / SCADA",
            "query": "What security requirements apply to SCADA systems?",
            "model": "gemini-3.1-flash-lite",
            "top_k": 30
        },

        {
            "query_id": "Q12",
            "category": "Monitoring",
            "query": "What events should be logged in ICS environments?",
            "model": "gpt-5.4-nano",
            "top_k": 20
        },

        {
            "query_id": "Q15",
            "category": "Governance",
            "query": "How should OT cybersecurity governance be established?",
            "model": "gpt-5.4-nano",
            "top_k": 20
        }
    ],


    "Evaluator C": [

        {
            "query_id": "Q03",
            "category": "Authentication",
            "query": "How should user authentication be implemented in ICS systems?",
            "model": "gpt-5.4-nano",
            "top_k": 10
        },

        {
            "query_id": "Q06",
            "category": "Backup & Recovery",
            "query": "What recovery procedures should be established for industrial systems?",
            "model": "gpt-5.4-nano",
            "top_k": 20
        },

        {
            "query_id": "Q11",
            "category": "Monitoring",
            "query": "How should security monitoring be implemented in OT?",
            "model": "gpt-5.4-nano",
            "top_k": 10
        },

        {
            "query_id": "Q16",
            "category": "Governance",
            "query": "What responsibilities should OT security roles have?",
            "model": "gpt-5.4-nano",
            "top_k": 30
        }
    ],


    "Evaluator D": [

        {
            "query_id": "Q05",
            "category": "Backup & Recovery",
            "query": "How should OT backups be protected?",
            "model": "gpt-5.4-nano",
            "top_k": 10
        },

        {
            "query_id": "Q08",
            "category": "ICS / SCADA",
            "query": "How should ICS assets be identified and managed?",
            "model": "gpt-5.4-nano",
            "top_k": 20
        },

        {
            "query_id": "Q10",
            "category": "Network Segmentation",
            "query": "What is the role of security zones and conduits?",
            "model": "gpt-5.4-nano",
            "top_k": 10
        },

        {
            "query_id": "Q13",
            "category": "OT Security Controls",
            "query": "What security controls protect industrial systems?",
            "model": "gemini-3.1-flash-lite",
            "top_k": 30
        }
    ]
}