
from numpy import place
import pandas as pd
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.optimizer import FuelOptimizer
from geopy.geocoders import Nominatim

@api_view(["GET"])
def health_check(request):
    return Response({
        "status": "success",
        "message": "Fuel Route API is working"
    })

@api_view(["GET"])
def fuel_data_sample(request):
    try:
        df = pd.read_csv("fuel_prices.csv")

        sample = df.head(5).to_dict(orient="records")

        return Response({
            "total_records": len(df),
            "sample_data": sample
        })

    except Exception as e:
        return Response({
            "error": str(e)
        })


@api_view(["POST"])
def get_route(request):
    try:
        start = request.data.get("start")
        finish = request.data.get("finish")

        if not start or not finish:
            return Response({"error": "start and finish are required"}, status=400)

        # STEP 1: Geocode start & finish
        def geocode(place):
            url = "https://api.openrouteservice.org/geocode/search"
            params = {
                "api_key": settings.OPENROUTE_API_KEY,
                "text": place,
                "boundary.country": "USA",
                "size": 1
            }

            res = requests.get(url, params=params)
            data = res.json()

            if not data["features"]:
                raise Exception(f"Location not found: {place}")

            return data["features"][0]["geometry"]["coordinates"]

        start_coords = geocode(start)
        finish_coords = geocode(finish)

        # STEP 2: Get route
        url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"

        headers = {
            "Authorization": settings.OPENROUTE_API_KEY,
            "Content-Type": "application/json"
        }

        body = {
            "coordinates": [start_coords, finish_coords]
        }

        res = requests.post(url, json=body, headers=headers)
        route_data = res.json()

        distance_meters = route_data["features"][0]["properties"]["summary"]["distance"]
        distance_miles = distance_meters / 1609.34

        coordinates = route_data["features"][0]["geometry"]["coordinates"]

        return Response({
            "start": start,
            "finish": finish,
            "distance_miles": round(distance_miles, 2),
            "route_points": coordinates[:10]  # only first 10 points for now
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(["POST"])
def fuel_route(request):
    try:
        start = request.data.get("start")
        finish = request.data.get("finish")

        if not start or not finish:
            return Response({"error": "start and finish are required"}, status=400)

        # Reuse existing route API logic
        def geocode(place):
            geolocator = Nominatim(user_agent="fuel_route_optimizer_app")
            location = geolocator.geocode(f"{place}, USA")

            if not location:
                raise Exception(f"Location not found: {place}")

            return [location.longitude, location.latitude]
        

        start_coords = geocode(start)
        finish_coords = geocode(finish)

        route_url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"

        headers = {
            "Authorization": settings.OPENROUTE_API_KEY,
            "Content-Type": "application/json"
        }

        body = {
            "coordinates": [start_coords, finish_coords]
        }

        res = requests.post(route_url, json=body, headers=headers)
        route_data = res.json()

        distance_meters = route_data["features"][0]["properties"]["summary"]["distance"]
        distance_miles = distance_meters / 1609.34
        route_points = route_data["features"][0]["geometry"]["coordinates"]

        optimizer = FuelOptimizer()

        fuel_stops = optimizer.calculate_stops(
            total_distance_miles=distance_miles,
            route_points=route_points
        )

        total_cost = optimizer.calculate_total_cost(
            stops=fuel_stops,
            total_distance_miles=distance_miles
        )

        return Response({
            "start": start,
            "finish": finish,
            "total_distance_miles": round(distance_miles, 2),
            "vehicle_range_miles": 500,
            "miles_per_gallon": 10,
            "optimization_note": "Fuel stops are selected by finding the cheapest available fuel station near each 500-mile route segment.",
            "api_usage": {
                "routing_api_calls": 1,
                "geocoding": "Handled separately using Nominatim geocoder",
                "fuel_data_source": "Local preprocessed CSV"
            },
            "fuel_stops": fuel_stops,
            "total_fuel_cost_usd": total_cost,
            "route_map": {
                "type": "LineString",
                "total_coordinates": len(route_points),
                "coordinates": route_points
            }
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)