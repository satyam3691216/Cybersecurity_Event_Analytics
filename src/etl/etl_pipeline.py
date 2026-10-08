import pandas as pd
from sqlalchemy import text

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

    # Keep only columns required by the security_events table
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
    print("\nColumn data types:")
    print(df[["user_id", "device_id", "ip_address"]].dtypes)

    print("\nSample ID values:")
    print(df[["user_id", "device_id", "ip_address"]].head())
    
def load_reference_data(df):
    """
    Load users, devices, and IP addresses required by security_events.
    Existing records are skipped.
    """
    from src.database.db_connection import engine

    print("Loading reference data...")

    with engine.begin() as connection:

        # Users
        users = df[["user_id"]].drop_duplicates()

        for _, row in users.iterrows():
            connection.execute(
                text("""
                    INSERT INTO users (
                        user_id,
                        username,
                        department,
                        role,
                        account_status,
                        created_at
                    )
                    VALUES (
                        :user_id,
                        :username,
                        'General',
                        'User',
                        'Active',
                        :created_at
                    )
                    ON CONFLICT (user_id) DO NOTHING
                """),
                {
                    "user_id": int(row["user_id"]),
                    "username": f"user_{int(row['user_id'])}",
                    "created_at": df["event_timestamp"].min()
                }
            )

        # Devices
        devices = df[
            ["device_id", "user_id", "device_type", "os"]
        ].drop_duplicates(subset=["device_id"])

        for _, row in devices.iterrows():
            connection.execute(
                text("""
                    INSERT INTO devices (
                        device_id,
                        user_id,
                        device_type,
                        operating_system,
                        device_name,
                        first_seen,
                        last_seen,
                        device_status
                    )
                    VALUES (
                        :device_id,
                        :user_id,
                        :device_type,
                        :operating_system,
                        :device_name,
                        :first_seen,
                        :last_seen,
                        'Active'
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

        # IP addresses
        ip_addresses = df[
            ["ip_address", "location"]
        ].drop_duplicates(subset=["ip_address"])

        for _, row in ip_addresses.iterrows():
            connection.execute(
                text("""
                    INSERT INTO ip_addresses (
                        ip_address,
                        country,
                        city,
                        region,
                        isp,
                        ip_type,
                        first_seen,
                        last_seen
                    )
                    VALUES (
                        :ip_address,
                        'India',
                        :city,
                        'Unknown',
                        'Synthetic ISP',
                        'Private',
                        :first_seen,
                        :last_seen
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
    load_data(df)