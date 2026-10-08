import pandas as pd


def extract_data(file_path):
    """
    Extract raw cybersecurity event data from a CSV file.
    """
    print("Extracting data...")

    df = pd.read_csv(file_path)

    print(f"Extracted {len(df)} records.")

    return df


def transform_data(df):
    """
    Perform basic data cleaning and transformation.
    """
    print("Transforming data...")

    df = df.copy()

    # Convert timestamp to datetime
    df["event_timestamp"] = pd.to_datetime(
        df["event_timestamp"],
        errors="coerce"
    )

    # Remove rows with invalid timestamps
    df = df.dropna(subset=["event_timestamp"])

    # Remove duplicate event IDs
    df = df.drop_duplicates(subset=["event_id"])

    # Standardize text columns
    text_columns = [
        "event_type",
        "location",
        "device_type",
        "os",
        "auth_status"
    ]

    for column in text_columns:
        df[column] = df[column].astype(str).str.strip()

    print(f"Records after transformation: {len(df)}")

    return df


if __name__ == "__main__":
    file_path = "data/raw/security_events_raw.csv"

    df = extract_data(file_path)

    df = transform_data(df)

    print("\nTransformed data:")
    print(df.head())