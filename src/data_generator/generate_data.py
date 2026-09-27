# Synthetic Cybersecurity Event Data Generator

import numpy as np
import pandas as pd


def generate_security_events(num_events=1000):
    np.random.seed(42)

    print(f"Generating {num_events} cybersecurity events...")

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

    security_events = pd.DataFrame({
        
        "event_id": range(1, num_events + 1),
        "event_timestamp": pd.date_range(start="2026-01-01",periods=num_events,freq="min"),
        "event_type": np.random.choice(event_types, num_events),
        "user_id": np.random.randint(1001, 1101, num_events),
        "device_id": np.random.randint(2001, 2051, num_events),
        "ip_address": [
            f"192.168.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}"
            for _ in range(num_events)
        ],
        "location": np.random.choice(["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Pune", "Chennai", "Kolkata"],num_events),
        "device_type": np.random.choice(["Laptop", "Desktop", "Mobile", "Tablet"],num_events),
        "os": np.random.choice(["Windows", "macOS", "Linux", "Android", "iOS"],num_events),
        "auth_status": np.random.choice(["Success", "Failed"],num_events,p=[0.85, 0.15]),
        "user_agent": np.random.choice([
        "Chrome",
        "Firefox",
        "Edge",
        "Safari",
        "MobileApp"],num_events),
        "session_id": [
    f"SESSION_{np.random.randint(10000, 20000)}"
    for _ in range(num_events)
],
"risk_indicator": np.random.choice(
    ["Low", "Medium", "High"],
    num_events,
    p=[0.70, 0.25, 0.05]
)
    })
    return security_events


if __name__ == "__main__":
    df = generate_security_events(1000)
    print(df.head())