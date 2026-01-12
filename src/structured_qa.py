import pandas as pd

df = pd.read_csv("data/tables/ml_metrics.csv")

def answer_structured_query(query):
    q = query.lower()

    if "average latency" in q:
        return f"The average model latency is {df['latency_ms'].mean():.1f} ms."

    if "highest accuracy" in q:
        row = df.loc[df['accuracy'].idxmax()]
        return f"The model with the highest accuracy is {row['model_name']} ({row['accuracy']})."

    if "incidents" in q:
        recent = df.sort_values("last_incident_days").iloc[0]
        return (
            f"The most recent incident occurred in model "
            f"{recent['model_name']} ({recent['last_incident_days']} days ago)."
        )

    return "I don't know based on the available structured data."
