import os
import time
import pandas as pd
import requests

API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImVhN2YzMWE4YmQ3YTQwMjhhNjVmNmJmMDA2Zjc3OTQwIiwiaCI6Im11cm11cjY0In0="

INPUT_FILE = "fuel_prices.csv"
OUTPUT_FILE = "fuel_prices_with_coordinates.csv"


def geocode(address):
    url = "https://api.openrouteservice.org/geocode/search"

    params = {
        "api_key": API_KEY,
        "text": address,
        "boundary.country": "USA",
        "size": 1
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        data = response.json()

        if "features" in data and data["features"]:
            lon, lat = data["features"][0]["geometry"]["coordinates"]
            return lat, lon

        return None, None

    except Exception as e:
        print("Error:", e)
        return None, None


def main():
    original_df = pd.read_csv(INPUT_FILE)

    if os.path.exists(OUTPUT_FILE):
        existing_df = pd.read_csv(OUTPUT_FILE)
        print("Continuing from existing output file...")

        original_df["latitude"] = None
        original_df["longitude"] = None

        for i in range(min(len(existing_df), len(original_df))):
            original_df.at[i, "latitude"] = existing_df.at[i, "latitude"]
            original_df.at[i, "longitude"] = existing_df.at[i, "longitude"]

        df = original_df
    else:
        df = original_df
        df["latitude"] = None
        df["longitude"] = None

    print("Total rows to process:", len(df))
    print("Already geocoded:", df["latitude"].notna().sum())

    for i, row in df.iterrows():
        if pd.notna(row["latitude"]) and pd.notna(row["longitude"]):
            continue

        full_address = f"{row['Address']}, {row['City']}, {row['State']}, USA"

        lat, lon = geocode(full_address)

        df.at[i, "latitude"] = lat
        df.at[i, "longitude"] = lon

        print(f"{i} → {full_address} → {lat}, {lon}")

        if i % 10 == 0:
            df.to_csv(OUTPUT_FILE, index=False)
            print("Progress saved...")

        time.sleep(1)

    df.to_csv(OUTPUT_FILE, index=False)
    print("Geocoding completed!")


if __name__ == "__main__":
    main()