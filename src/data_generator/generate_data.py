# Synthetic Cybersecurity Event Data Generator

import numpy as np
import pandas as pd
from pathlib import Path


def generate_security_events(num_events=1000):
    """Generate synthetic cybersecurity events."""

    np.random.seed(42)

    print(f"Generating {num_events} cybersecurity events...")

    # --------------------------------------------------
    # 1. Generate users and assign fixed device owners
    # --------------------------------------------------

    user_ids_available = np.arange(1001, 1101)
    device_ids_available = np.arange(2001, 2051)

    # Assign each device to exactly one user
    device_owners = np.random.choice(
        user_ids_available,
        size=len(device_ids_available),
        replace=True
    )

    device_owner = dict(
        zip(device_ids_available, device_owners)
    )

    # Select devices for security events
    device_ids = np.random.choice(
        device_ids_available,
        size=num_events
    )

    # Every device retains its assigned owner
    user_ids = np.array([
        device_owner[device_id]
        for device_id in device_ids
    ])
    # Assign the first five events to one device and its owner
    if num_events >= 5:
        suspicious_device_id = device_ids_available[0]
        suspicious_user_id = device_owner[suspicious_device_id]

        device_ids[:5] = suspicious_device_id
        user_ids[:5] = suspicious_user_id
    # --------------------------------------------------
    # 2. Define event types
    # --------------------------------------------------

    event_types = [
        "login_success",
        "login_failed",
        "logout",
        "password_change",
        "account_locked",
        "file_access",
        "file_download",
        "api_access",
        "device_login",
        "admin_action"
    ]

    # Generate event types once so authentication status
    # can be derived consistently from the same values.
    event_types_generated = np.random.choice(
        event_types,
        size=num_events
    )
    # Inject controlled suspicious-login scenarios
    if num_events >= 5:
        suspicious_device_id = device_ids_available[0]
        suspicious_user_id = device_owner[suspicious_device_id]

        suspicious_indices = np.arange(5)

    for index in suspicious_indices:
        event_types_generated[index] = "login_failed"
        user_ids[index] = suspicious_user_id
        device_ids[index] = suspicious_device_id

    # Select 5 events to simulate repeated failed logins
    suspicious_indices = np.arange(min(5, num_events))

    for index in suspicious_indices:
        event_types_generated[index] = "login_failed"
        user_ids[index] = suspicious_user_id
        device_ids[index] = suspicious_device_id

    # --------------------------------------------------
    # 3. Generate authentication status
    # --------------------------------------------------

    auth_status = []

    for event_type in event_types_generated:

        if event_type == "login_failed":
            auth_status.append("Failed")

        elif event_type == "login_success":
            auth_status.append("Success")

        else:
            # Other event types may have either status.
            status = np.random.choice(
                ["Success", "Failed"],
                p=[0.85, 0.15]
            )

            auth_status.append(status)
    # Ensure injected suspicious events have consistent authentication status
    if num_events >= 5:
        auth_status[:5] = ["Failed"] * 5
    # --------------------------------------------------
    # 4. Generate synthetic security events
    # --------------------------------------------------

    security_events = pd.DataFrame({

        "event_id": range(1, num_events + 1),

        "event_timestamp": pd.date_range(
            start="2026-01-01",
            periods=num_events,
            freq="min"
        ),

        "event_type": event_types_generated,

        "user_id": user_ids,

        "device_id": device_ids,

        "ip_address": [
            (
                f"192.168."
                f"{np.random.randint(1, 255)}."
                f"{np.random.randint(1, 255)}"
            )
            for _ in range(num_events)
        ],

        "location": np.random.choice(
            [
                "Delhi",
                "Mumbai",
                "Bangalore",
                "Hyderabad",
                "Pune",
                "Chennai",
                "Kolkata"
            ],
            size=num_events
        ),

        "device_type": np.random.choice(
            [
                "Laptop",
                "Desktop",
                "Mobile",
                "Tablet"
            ],
            size=num_events
        ),

        "os": np.random.choice(
            [
                "Windows",
                "macOS",
                "Linux",
                "Android",
                "iOS"
            ],
            size=num_events
        ),

        "auth_status": auth_status,

        "user_agent": np.random.choice(
            [
                "Chrome",
                "Firefox",
                "Edge",
                "Safari",
                "MobileApp"
            ],
            size=num_events
        ),

        "session_id": [
            f"SESSION_{np.random.randint(10000, 20000)}"
            for _ in range(num_events)
        ],

        "risk_indicator": np.random.choice(
            [
                "Low",
                "Medium",
                "High"
            ],
            size=num_events,
            p=[0.70, 0.25, 0.05]
        )
    })

    print("Dataset generation completed.")
    print(f"Total events generated: {len(security_events)}")

    return security_events


# --------------------------------------------------
# 5. Run the generator and save the dataset
# --------------------------------------------------

if __name__ == "__main__":

    df = generate_security_events(1000)

    output_path = Path("data/raw/security_events_raw.csv")

    # Ensure the output directory exists
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save the generated dataset
    df.to_csv(
        output_path,
        index=False
    )

    print(f"Dataset saved to: {output_path}")

    print("\nFirst five records:")
    print(df.head())

    # --------------------------------------------------
    # 6. Verify device-to-user consistency
    # --------------------------------------------------

    device_user_counts = (
        df.groupby("device_id")["user_id"]
        .nunique()
    )

    inconsistent_devices = (
        device_user_counts > 1
    ).sum()

    print(
        "\nDevices associated with multiple users:",
        int(inconsistent_devices)
    )

    # --------------------------------------------------
    # 7. Verify authentication consistency
    # --------------------------------------------------

    failed_login_inconsistencies = (
        (
            (df["event_type"] == "login_failed")
            & (df["auth_status"] != "Failed")
        )
        |
        (
            (df["event_type"] == "login_success")
            & (df["auth_status"] != "Success")
        )
    ).sum()

    print(
        "Authentication inconsistencies:",
        int(failed_login_inconsistencies)
    )

    # --------------------------------------------------
    # 8. Report validation results
    # --------------------------------------------------

    if inconsistent_devices == 0:
        print("Device-to-user consistency check passed.")
    else:
        print("WARNING: Device-to-user inconsistency detected.")

    if failed_login_inconsistencies == 0:
        print("Authentication consistency check passed.")
    else:
        print("WARNING: Authentication inconsistencies detected.")