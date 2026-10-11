"""
ETL pipeline for the Cybersecurity Event Analytics project.

Workflow:
1. Extract synthetic security events from CSV.
2. Transform and clean the data.
3. Validate the transformed data.
4. Load reference data into PostgreSQL.
5. Load security events without duplicate event IDs.
"""

import pandas as pd

from sqlalchemy import MetaData, Table, text
from sqlalchemy.dialects.postgresql import insert

from src.database.db_connection import engine
from src.etl.data_validation import validate_security_events


# --------------------------------------------------
# 1. EXTRACT
# --------------------------------------------------

def extract_data(file_path):
    """Read cybersecurity events from a CSV file."""

    print("\n[1/5] Extracting data...")

    df = pd.read_csv(file_path)

    print(f"Records extracted: {len(df)}")

    return df


# --------------------------------------------------
# 2. TRANSFORM
# --------------------------------------------------

def transform_data(df):
    """Clean and prepare cybersecurity event data."""

    print("\n[2/5] Transforming data...")

    df = df.copy()

    # Convert timestamps to datetime
    df["event_timestamp"] = pd.to_datetime(
        df["event_timestamp"],
        errors="coerce"
    )

    # Remove records with invalid timestamps
    df = df.dropna(
        subset=["event_timestamp"]
    )

    # Remove duplicate event IDs
    df = df.drop_duplicates(
        subset=["event_id"]
    )

    # Clean text columns
    text_columns = [
        "event_type",
        "location",
        "device_type",
        "os",
        "auth_status"
    ]

    for column in text_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    # Remove the synthetic risk label from raw events.
    # Risk scoring will be developed separately.
    df = df.drop(
        columns=["risk_indicator"],
        errors="ignore"
    )

    # Select the required source columns
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

    # Match the PostgreSQL column name
    df = df.rename(
        columns={
            "os": "operating_system"
        }
    )

    # Convert numeric IDs to integer values
    df["event_id"] = df["event_id"].astype(int)
    df["user_id"] = df["user_id"].astype(int)
    df["device_id"] = df["device_id"].astype(int)

    print(f"Records after transformation: {len(df)}")

    return df


# --------------------------------------------------
# 3. LOAD REFERENCE DATA
# --------------------------------------------------

def load_reference_data(df):
    """
    Insert users, devices, and IP addresses before events.

    Existing reference records are preserved.
    """

    print("\n[4/5] Loading reference data...")

    with engine.begin() as connection:

        # ------------------------------------------
        # Users
        # ------------------------------------------

        users = df[
            ["user_id"]
        ].drop_duplicates()

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

        # ------------------------------------------
        # Devices
        # ------------------------------------------

        devices = df[
            [
                "device_id",
                "user_id",
                "device_type",
                "operating_system"
            ]
        ].drop_duplicates(
            subset=["device_id"]
        )

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
                    "operating_system": row["operating_system"],
                    "device_name": (
                        f"{row['device_type']}_Device"
                    ),
                    "first_seen": df["event_timestamp"].min(),
                    "last_seen": df["event_timestamp"].max()
                }
            )

        # ------------------------------------------
        # IP addresses
        # ------------------------------------------

        ip_addresses = df[
            ["ip_address", "location"]
        ].drop_duplicates(
            subset=["ip_address"]
        )

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


# --------------------------------------------------
# 4. LOAD SECURITY EVENTS
# --------------------------------------------------

def load_data(df, table_name="security_events"):
    """
    Insert security events into PostgreSQL.

    Existing event IDs are skipped using PostgreSQL
    ON CONFLICT DO NOTHING.
    """

    print("\n[5/5] Loading security events...")

    # Load the actual PostgreSQL table definition
    metadata = MetaData()

    events_table = Table(
        table_name,
        metadata,
        autoload_with=engine
    )

    # Match DataFrame columns to database columns
    expected_columns = [
        column.name
        for column in events_table.columns
        if column.name in df.columns
    ]

    missing_columns = [
        column.name
        for column in events_table.columns
        if column.name not in df.columns
        and not column.primary_key
        and column.server_default is None
        and not column.nullable
        and column.autoincrement is not True
    ]

    if missing_columns:
        raise ValueError(
            "Required database columns are missing from the "
            f"DataFrame: {missing_columns}"
        )

    # Build records using only columns present in the table
    records = df[expected_columns].to_dict(
        orient="records"
    )

    if not records:
        print("No events to load.")
        return

    # Insert events in batches
    inserted_count = 0
    batch_size = 250

    with engine.begin() as connection:

        for start in range(0, len(records), batch_size):

            batch = records[
                start:start + batch_size
            ]

            statement = insert(
                events_table
            ).values(batch)

            statement = statement.on_conflict_do_nothing(
                index_elements=["event_id"]
            )

            result = connection.execute(statement)

            inserted_count += result.rowcount

    print(f"Records processed: {len(records)}")
    print(f"New events inserted: {inserted_count}")
    print(
        f"Existing events skipped: "
        f"{len(records) - inserted_count}"
    )


# --------------------------------------------------
# 5. MAIN PIPELINE
# --------------------------------------------------

if __name__ == "__main__":

    file_path = "data/raw/security_events_raw.csv"

    try:

        # Extract
        df = extract_data(file_path)

        # Transform
        df = transform_data(df)

        # Validate
        print("\n[3/5] Validating data...")

        validate_security_events(df)

        # Load reference tables first
        load_reference_data(df)

        # Load events
        load_data(df)

        print("\nETL pipeline completed successfully.")

    except Exception as error:

        print("\nETL pipeline failed.")
        print(f"Error: {error}")

        raise