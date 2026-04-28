from .fuel_service import FuelService


class FuelOptimizer:
    VEHICLE_RANGE_MILES = 500
    MPG = 10

    def __init__(self):
        self.fuel_service = FuelService()

    def get_route_point(self, route_points, percentage):
        index = int(len(route_points) * percentage)

        if index >= len(route_points):
            index = len(route_points) - 1

        lon, lat = route_points[index]
        return lat, lon

    def calculate_stops(self, total_distance_miles, route_points):
        stops = []
        current_mile = self.VEHICLE_RANGE_MILES

        while current_mile < total_distance_miles:
            percentage = current_mile / total_distance_miles

            lat, lon = self.get_route_point(route_points, percentage)

            station = self.fuel_service.find_cheapest_nearby_station(
                lat,
                lon,
                radius_miles=100
            )

            if station:
                gallons = self.VEHICLE_RANGE_MILES / self.MPG
                cost = gallons * station["retail_price"]

                stops.append({
                    "stop_number": len(stops) + 1,
                    "approx_mile": round(current_mile, 2),
                    "gallons": round(gallons, 2),
                    "cheapest_nearby_fuel_station": station,
                    "estimated_cost": round(cost, 2)
                })

            current_mile += self.VEHICLE_RANGE_MILES

        return stops

    def calculate_total_cost(self, stops, total_distance_miles):
        total_cost = 0

        for stop in stops:
            total_cost += stop["estimated_cost"]

        remaining_distance = total_distance_miles % self.VEHICLE_RANGE_MILES

        if stops and remaining_distance > 0:
            last_price = stops[-1]["cheapest_nearby_fuel_station"]["retail_price"]
            total_cost += (remaining_distance / self.MPG) * last_price

        return round(total_cost, 2)