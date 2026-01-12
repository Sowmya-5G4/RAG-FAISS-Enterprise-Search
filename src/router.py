def classify_query(query):
    if any(word in query.lower() for word in ["how many", "count", "total"]):
        return "analytical"
    return "semantic"
