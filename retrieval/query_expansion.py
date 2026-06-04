def expand_query(query):
    query_lower = query.lower()
    expansion_map = {
        "plc": [
            "plc", "ics", "scada", "industrial control system",
            "control system", "ot security"
        ],
        "remote": [
            "remote access", "external connection", "vpn",
            "remote authentication", "remote session"
        ],
        "backup": [
            "backup", "restore", "recovery",
            "continuity", "resilience", "redundancy"
        ],
        "segmentation": [
            "segmentation", "zone", "boundary",
            "isolation", "network separation"
        ],
        "access": [
            "access control", "authentication",
            "authorization", "identity", "privilege"
        ],
        "monitoring": [
            "monitoring", "logging", "alerting",
            "detection", "event analysis","vulnerability"
        ]
    }
    expanded_query = query
    for key, words in expansion_map.items():
        if key in query_lower:
            expanded_query+= " "+ " ".join(words)
    return expanded_query
