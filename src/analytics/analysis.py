"""
End-to-end cybersecurity analytics workflow.

Combines:
1. PostgreSQL event extraction
2. Rule-based risk scoring
3. Isolation Forest anomaly detection
4. Hybrid risk scoring
5. Automated alert generation
6. Alert storage in PostgreSQL
"""

from src.risk_engine.risk_scoring import (
    fetch_security_events,
    calculate_event_risk,
    calculate_hybrid_risk,
)

from src.anomaly_detection.anomaly_detector import detect_anomalies

from src.alerts.alert_manager import (
    generate_alerts,
    save_alerts,
)


def run_security_analytics():
    """Execute the complete security analytics workflow."""

    print("\n" + "=" * 50)
    print("CYBERSECURITY EVENT ANALYTICS SYSTEM")
    print("=" * 50)

    # Step 1: Fetch security events.
    df = fetch_security_events()

    if df.empty:
        print("No security events available.")
        return

    # Step 2: Calculate rule-based risk scores.
    print("\nCalculating rule-based risk scores...")
    df = calculate_event_risk(df)

    # Step 3: Detect anomalies.
    print("\nDetecting anomalous events...")
    df = detect_anomalies(df)

    # Step 4: Calculate hybrid risk scores.
    print("\nCalculating hybrid risk scores...")
    df = calculate_hybrid_risk(df)

    # Step 5: Generate alerts.
    print("\nGenerating security alerts...")
    alerts = generate_alerts(df)

    # Step 6: Store alerts in PostgreSQL.
    print("\nSaving alerts to PostgreSQL...")
    saved_alerts = save_alerts(alerts)

    # Step 7: Display the analytics summary.
    print("\n" + "=" * 50)
    print("SECURITY ANALYTICS SUMMARY")
    print("=" * 50)

    print(f"Total events analysed: {len(df)}")
    print(f"Anomalies detected: {int(df['is_anomaly'].sum())}")
    print(f"Alerts generated: {len(alerts)}")
    print(f"New alerts saved: {saved_alerts}")

    print("\nRisk-level distribution:")
    print(df["hybrid_risk_level"].value_counts().to_string())

    print("\nTop 10 highest-risk events:")

    columns = [
        "event_id",
        "user_id",
        "event_type",
        "hybrid_score",
        "hybrid_risk_level",
    ]

    print(
        df.nlargest(10, "hybrid_score")[columns]
        .to_string(index=False)
    )

    print("\nAnalytics workflow completed.")


if __name__ == "__main__":
    run_security_analytics()