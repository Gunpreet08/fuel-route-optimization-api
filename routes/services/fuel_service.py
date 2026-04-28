import pandas as pd
import math


class FuelService:
    def __init__(self):
        self.df = pd.read_csv("fuel_prices_with_coordinates.csv")
        self.df = self.df.dropna(subset=["latitude", "longitude", "Retail Price"])

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        radius = 3958.8

        lat1 = math.radians(float(lat1))
        lon1 = math.radians(float(lon1))
        lat2 = math.radians(float(lat2))
        lon2 = math.radians(float(lon2))

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return radius * c

    def find_cheapest_nearby_station(self, lat, lon, radius_miles=75):
        nearby = []

        for _, row in self.df.iterrows():
            distance = self.calculate_distance(
                lat,
                lon,
                row["latitude"],
                row["longitude"]
            )

            if distance <= radius_miles:
                nearby.append({
                    "city": row["City"],
                    "state": row["State"],
                    "retail_price": float(row["Retail Price"]),
                    "latitude": float(row["latitude"]),
                    "longitude": float(row["longitude"]),
                    "distance_from_route_miles": round(distance, 2)
                })

        if not nearby:
            return None

        return min(nearby, key=lambda x: x["retail_price"])