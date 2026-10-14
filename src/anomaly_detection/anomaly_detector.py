"""
Machine-learning anomaly detection using Isolation Forest.
"""

import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(df, contamination=0.05):
    """
    Identify unusual security events using Isolation Forest.

    Parameters
    ----------
    df : pandas.DataFrame
        Security events with numerical or categorical features.
    contamination : float
        Expected proportion of anomalies.

    Returns
    -------
    pandas.DataFrame
        Original events with anomaly predictions and scores.
    """

    df = df.copy()

    # Convert event categories into numerical features.
    features = pd.DataFrame(index=df.index)

    features["failed_login"] = (
        df["event_type"] == "login_failed"
    ).astype(int)

    features["successful_login"] = (
        df["event_type"] == "login_success"
    ).astype(int)

    features["auth_failed"] = (
        df["auth_status"] == "Failed"
    ).astype(int)

    features["hour_of_day"] = pd.to_datetime(
        df["event_timestamp"]
    ).dt.hour

    features["user_event_frequency"] = (
        df.groupby("user_id")["event_id"]
        .transform("count")
    )

    # Train the anomaly-detection model.
    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=42
    )

    predictions = model.fit_predict(features)

    # -1 means anomaly; 1 means normal.
    df["is_anomaly"] = (predictions == -1).astype(int)

    # Higher anomaly scores indicate more unusual events.
    df["anomaly_score"] = -model.decision_function(features)

    print(f"Events analysed: {len(df)}")
    print(f"Anomalies detected: {df['is_anomaly'].sum()}")

    return df