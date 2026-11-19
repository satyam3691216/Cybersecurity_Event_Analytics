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
        "operating_system",
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