"""
Rule-based risk scoring for cybersecurity events.
"""

import pandas as pd
from sqlalchemy import text
from src.database.db_connection import engine


def calculate_risk_score(
    failed_logins: int = 0,
    new_ip: bool = False,
    new_device: bool = False,
) -> int:
    """
    Calculate a risk score using configurable detection rules.

    Rules:
    - Failed login: +10 points
    - Five or more failed logins: +40 points
    - New IP address: +20 points
    - New device: +20 points

    The final score is capped at 100.
    """

    score = 0

    if failed_logins > 0:
        score += 10

    if failed_logins >= 5:
        score += 40

    if new_ip:
        score += 20

    if new_device:
        score += 20

    return min(score, 100)


def get_risk_level(score: int) -> str:
    """Classify a numeric risk score."""

    if score >= 70:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"
def fetch_security_events():
    """Fetch security events from PostgreSQL."""

    query = text("""
        SELECT
            event_id,
            event_timestamp,
            event_type,
            user_id,
            device_id,
            ip_address,
            auth_status
        FROM security_events
        ORDER BY event_timestamp
    """)

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    print(f"Security events fetched: {len(df)}")

    return df    
def calculate_event_risk(df):
    """Calculate rule-based risk scores for security events."""

    df = df.copy()

    # Count failed logins for each user within the preceding 5 minutes.
    failed_logins = df["event_type"].eq("login_failed")

    df["failed_logins_5min"] = 0

    for user_id, group in df.groupby("user_id"):
        user_failed = group.loc[failed_logins.loc[group.index]].sort_values(
            "event_timestamp"
        )

        for index, row in user_failed.iterrows():
            window_start = row["event_timestamp"] - pd.Timedelta(minutes=5)

            count = user_failed[
                (user_failed["event_timestamp"] >= window_start)
                & (user_failed["event_timestamp"] <= row["event_timestamp"])
            ].shape[0]

            df.loc[index, "failed_logins_5min"] = count

    # Calculate risk scores.
    df["rule_score"] = df.apply(
        lambda row: calculate_risk_score(
            failed_logins=row["failed_logins_5min"],
            new_ip=False,
            new_device=False,
        ),
        axis=1,
    )

    # Assign risk levels.
    df["risk_level"] = df["rule_score"].apply(get_risk_level)

    return df