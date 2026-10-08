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

    # Remove fields that are not part of the security_events database table
    df = df.drop(columns=["risk_indicator"], errors="ignore")

    print(f"Records after transformation: {len(df)}")

    return df

def load_data(df, table_name="security_events"):
    """
    Load transformed cybersecurity events into PostgreSQL.
    """
    print("Loading data into PostgreSQL...")

    from src.database.db_connection import engine

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(df)} records into {table_name}.")

if __name__ == "__main__":
    file_path = "data/raw/security_events_raw.csv"

    df = extract_data(file_path)

    df = transform_data(df)

    load_data(df)