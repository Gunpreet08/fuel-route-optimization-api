import pandas as pd

df = pd.read_csv("fuel_prices_with_coordinates.csv")

df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
df["Retail Price"] = pd.to_numeric(df["Retail Price"], errors="coerce")

df = df.dropna(subset=["latitude", "longitude", "Retail Price"])

df.to_csv("fuel_prices_with_coordinates.csv", index=False)

print("Cleaned rows:", len(df))