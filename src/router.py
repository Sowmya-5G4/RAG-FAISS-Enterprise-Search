def classify_query(query):
    q = query.lower()

    structured_keywords = [
        # analytical / numerical
        "how many",
        "count",
        "total",
        "sum",
        "average",
        "avg",
        "maximum",
        "minimum",
        "highest",
        "lowest",

        # metrics-related
        "latency",
        "accuracy",
        "incidents",
        "requests",
        "metrics",
        "model performance"
    ]

    if any(word in q for word in structured_keywords):
        return "structured"

    return "semantic"
