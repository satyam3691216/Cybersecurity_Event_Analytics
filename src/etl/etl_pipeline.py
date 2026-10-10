import pandas as pd

from src.database.db_connection import engine
from src.etl.data_validation import validate_security_events


def extract_data(file_path):
    """Extract cybersecurity events from a CSV file."""
    print("Extracting data...")

    df = pd.read_csv(file_path)

    print(f"Extracted {len(df)} records.")

    return df


def transform_data(df):
    """Clean and prepare cybersecurity event data."""
    print("Transforming data...")

    df = df.copy()

    df["event_timestamp"] = pd.to_datetime(
        df["event_timestamp"],
        errors="coerce"
    )

    df = df.dropna(subset=["event_timestamp"])

    df = df.drop_duplicates(subset=["event_id"])

    text_columns = [
        "event_type",
        "location",
        "device_type",
        "os",
        "auth_status"
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    df = df.drop(columns=["risk_indicator"], errors="ignore")

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

    df = df[required_columns]

    print(f"Records after transformation: {len(df)}")

    return df


def load_reference_data(df):
    """Load users, devices, and IP addresses before security events."""

    print("Loading reference data...")

    with engine.begin() as connection:

        users = df[["user_id"]].drop_duplicates()

        for _, row in users.iterrows():
            connection.execute(
                __import__("sqlalchemy").text("""
                    INSERT INTO users (
                        user_id, username, department,
                        role, account_status, created_at
                    )
                    VALUES (
                        :user_id, :username, 'General',
                        'User', 'Active', :created_at
                    )
                    ON CONFLICT (user_id) DO NOTHING
                """),
                {
                    "user_id": int(row["user_id"]),
                    "username": f"user_{int(row['user_id'])}",
                    "created_at": df["event_timestamp"].min()
                }
            )

        devices = df[
            ["device_id", "user_id", "device_type", "os"]
        ].drop_duplicates(subset=["device_id"])

        for _, row in devices.iterrows():
            connection.execute(
                __import__("sqlalchemy").text("""
                    INSERT INTO devices (
                        device_id, user_id, device_type,
                        operating_system, device_name,
                        first_seen, last_seen, device_status
                    )
                    VALUES (
                        :device_id, :user_id, :device_type,
                        :operating_system, :device_name,
                        :first_seen, :last_seen, 'Active'
                    )
                    ON CONFLICT (device_id) DO NOTHING
                """),
                {
                    "device_id": int(row["device_id"]),
                    "user_id": int(row["user_id"]),
                    "device_type": row["device_type"],
                    "operating_system": row["os"],
                    "device_name": f"{row['device_type']}_Device",
                    "first_seen": df["event_timestamp"].min(),
                    "last_seen": df["event_timestamp"].max()
                }
            )

        ip_addresses = df[
            ["ip_address", "location"]
        ].drop_duplicates(subset=["ip_address"])

        for _, row in ip_addresses.iterrows():
            connection.execute(
                __import__("sqlalchemy").text("""
                    INSERT INTO ip_addresses (
                        ip_address, country, city, region,
                        isp, ip_type, first_seen, last_seen
                    )
                    VALUES (
                        :ip_address, 'India', :city, 'Unknown',
                        'Synthetic ISP', 'Private',
                        :first_seen, :last_seen
                    )
                    ON CONFLICT (ip_address) DO NOTHING
                """),
                {
                    "ip_address": row["ip_address"],
                    "city": row["location"],
                    "first_seen": df["event_timestamp"].min(),
                    "last_seen": df["event_timestamp"].max()
                }
            )

    print("Reference data loaded successfully.")


def load_data(df, table_name="security_events"):
    """Load transformed events into PostgreSQL."""
    print("Loading data into PostgreSQL...")

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

    validate_security_events(df)

    load_reference_data(df)

    load_data(df)