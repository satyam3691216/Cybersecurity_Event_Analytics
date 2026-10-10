import pandas as pd


def validate_security_events(df):
    """
    Validate the structure and quality of cybersecurity event data.
    """

    required_columns = [
        "event_id",
        "event_timestamp",
        "event_type",
        "user_id",
        "device_id",
        "ip_address",
        "location",
        "device_type",
        "os",
        "auth_status",
        "user_agent",
        "session_id"
    ]

    print("Running data quality checks...")

    # Check for missing columns
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Check for duplicate event IDs
    duplicate_events = df["event_id"].duplicated().sum()

    # Check for missing values
    missing_values = df[required_columns].isnull().sum().sum()

    # Check for invalid timestamps
    invalid_timestamps = df["event_timestamp"].isna().sum()

    print(f"Duplicate event IDs: {duplicate_events}")
    print(f"Missing values: {missing_values}")
    print(f"Invalid timestamps: {invalid_timestamps}")

    if duplicate_events > 0:
        raise ValueError("Duplicate event IDs detected.")

    if missing_values > 0:
        raise ValueError("Missing values detected.")

    if invalid_timestamps > 0:
        raise ValueError("Invalid timestamps detected.")

    print("Data quality validation passed.")

    return True
if __name__ == "__main__":
    sample_data = {
        "event_id": [1, 2, 3],
        "event_timestamp": pd.to_datetime([
            "2026-01-01 10:00:00",
            "2026-01-01 10:05:00",
            "2026-01-01 10:10:00"
        ]),
        "event_type": ["login", "logout", "login"],
        "user_id": [101, 102, 101],
        "device_id": [201, 202, 201],
        "ip_address": [
            "192.168.1.10",
            "192.168.1.11",
            "192.168.1.10"
        ],
        "location": ["Delhi", "Mumbai", "Delhi"],
        "device_type": ["Laptop", "Mobile", "Laptop"],
        "os": ["Windows", "Android", "Windows"],
        "auth_status": ["Success", "Success", "Failed"],
        "user_agent": ["Chrome", "Edge", "Chrome"],
        "session_id": ["S001", "S002", "S003"]
    }

    test_df = pd.DataFrame(sample_data)

    validate_security_events(test_df)