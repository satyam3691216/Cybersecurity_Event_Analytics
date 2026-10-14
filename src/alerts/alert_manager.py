"""
Automated alert generation for suspicious security events.
"""

import pandas as pd
from sqlalchemy import text
from src.database.db_connection import engine


def generate_alerts(df):
    """
    Generate alerts for events with medium or high hybrid risk.

    Required columns:
        event_id, user_id, event_type, hybrid_score, hybrid_risk_level

    Returns:
        DataFrame containing generated alerts.
    """

    required_columns = [
        "event_id",
        "user_id",
        "event_type",
        "hybrid_score",
        "hybrid_risk_level",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    alerts = df[
        df["hybrid_score"] >= 40
    ].copy()

    if alerts.empty:
        print("No alerts generated.")
        return pd.DataFrame(
            columns=[
                "event_id",
                "user_id",
                "alert_type",
                "alert_message",
                "severity",
            ]
        )

    alerts["alert_type"] = "Suspicious Security Activity"

    alerts["alert_message"] = alerts.apply(
        lambda row: (
            f"Suspicious event '{row['event_type']}' detected "
            f"for user {row['user_id']}. "
            f"Hybrid risk score: {row['hybrid_score']}."
        ),
        axis=1,
    )

    alerts["severity"] = alerts["hybrid_score"].apply(
        lambda score: (
            "High" if score >= 70 else "Medium"
        )
    )

    result = alerts[
        [
            "event_id",
            "user_id",
            "alert_type",
            "alert_message",
            "severity",
        ]
    ].reset_index(drop=True)

    print(f"Alerts generated: {len(result)}")

    return result
def save_alerts(alerts):
    if alerts.empty:
        print("No alerts to save.")
        return 0

    query = text("""
        INSERT INTO alerts (
            event_id,
            alert_type,
            alert_message,
            severity,
            alert_status,
            created_at
        )
        SELECT
            :event_id,
            :alert_type,
            :alert_message,
            :severity,
            'Open',
            CURRENT_TIMESTAMP
        WHERE NOT EXISTS (
            SELECT 1
            FROM alerts
            WHERE event_id = :event_id
              AND alert_type = :alert_type
        )
    """)

    records = alerts[
        ["event_id", "alert_type", "alert_message", "severity"]
    ].to_dict(orient="records")

    with engine.begin() as connection:
        result = connection.execute(query, records)

    saved_count = result.rowcount

    print(f"New alerts saved: {saved_count}")
    print(f"Duplicate alerts skipped: {len(alerts) - saved_count}")

    return saved_count