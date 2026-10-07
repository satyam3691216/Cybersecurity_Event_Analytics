import pandas as pd


def extract_data(file_path):
    """
    Extract raw cybersecurity event data from a CSV file.
    """
    print("Extracting data...")

    df = pd.read_csv(file_path)

    print(f"Extracted {len(df)} records.")

    return df


if __name__ == "__main__":
    file_path = "data/raw/security_events_raw.csv"

    df = extract_data(file_path)

    print("\nFirst 5 records:")
    print(df.head())