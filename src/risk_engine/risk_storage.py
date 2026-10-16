from sqlalchemy import text
from src.database.db_connection import engine


def save_risk_scores(df):
    """
    Save calculated risk scores to PostgreSQL.

    Required DataFrame columns:
    event_id, rule_score, anomaly_score,
    hybrid_score, hybrid_risk_level
    """

    required_columns = [
        "event_id",
        "rule_score",
        "anomaly_score",
        "hybrid_score",
        "hybrid_risk_level",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    query = text("""
        INSERT INTO risk_events (
            event_id,
            rule_score,
            anomaly_score,
            hybrid_score,
            risk_level
        )
        VALUES (
            :event_id,
            :rule_score,
            :anomaly_score,
            :hybrid_score,
            :risk_level
        )
        ON CONFLICT DO NOTHING
    """)

    records = df[required_columns].rename(
        columns={
            "hybrid_risk_level": "risk_level"
        }
    ).to_dict(orient="records")

    with engine.begin() as connection:
        result = connection.execute(query, records)

    saved_count = result.rowcount

    print(f"Risk records saved: {saved_count}")

    return saved_count