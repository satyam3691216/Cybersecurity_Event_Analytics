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

    # --------------------------------------------------
    # 2. Define security event types
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

    # --------------------------------------------------
    # 3. Generate synthetic security events
    # --------------------------------------------------

    security_events = pd.DataFrame({

        "event_id": range(1, num_events + 1),

        "event_timestamp": pd.date_range(
            start="2026-01-01",
            periods=num_events,
            freq="min"
        ),

        "event_type": np.random.choice(
            event_types,
            num_events
        ),

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
            num_events
        ),

        "device_type": np.random.choice(
            [
                "Laptop",
                "Desktop",
                "Mobile",
                "Tablet"
            ],
            num_events
        ),

        "os": np.random.choice(
            [
                "Windows",
                "macOS",
                "Linux",
                "Android",
                "iOS"
            ],
            num_events
        ),

        "auth_status": np.random.choice(
            [
                "Success",
                "Failed"
            ],
            num_events,
            p=[0.85, 0.15]
        ),

        "user_agent": np.random.choice(
            [
                "Chrome",
                "Firefox",
                "Edge",
                "Safari",
                "MobileApp"
            ],
            num_events
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
            num_events,
            p=[0.70, 0.25, 0.05]
        )
    })

    print("Dataset generation completed.")
    print(f"Total events generated: {len(security_events)}")

    return security_events


# --------------------------------------------------
# 4. Run the generator and save the dataset
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
    # 5. Verify device-to-user consistency
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

    if inconsistent_devices == 0:
        print("Device-to-user consistency check passed.")
    else:
        print("WARNING: Device-to-user inconsistency detected.")