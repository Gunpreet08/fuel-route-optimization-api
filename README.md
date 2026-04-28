# 🚀 Fuel Route Optimization API
This project is a Django REST API that calculates optimal fuel stops along a route within the USA based on fuel prices.


## 🔧 Features
- Accepts start and destination locations
- Calculates route using OpenRouteService
- Determines fuel stops every 500 miles
- Selects cheapest fuel station near route
- Estimates total fuel cost (10 MPG)
- Returns route geometry for map visualization


## ⚙️ Optimization Strategy
- Only 1 routing API call is used (OpenRouteService)
- Fuel data is loaded from a local preprocessed dataset
- Geocoding handled separately using Nominatim
- Minimizes latency and external API usage


## 📊 Data Handling
- Fuel dataset enriched with latitude & longitude using preprocessing
- Invalid entries removed for accurate calculations
- Uses ~983 valid fuel stations


## 🧪 API Endpoint
POST /api/fuel-route/
### Request:
```
{
  "start": "Dallas, TX",
  "finish": "Chicago, IL"
}
```

### Response includes:
- Distance
- Fuel stops
- Cheapest stations
- Cost per stop
- Total fuel cost
- Route geometry


## 🛠️ Tech Stack
- Django REST Framework
- OpenRouteService API
- Nominatim (Geocoding)
- Pandas (data processing)


## ▶️ Run Locally
```
git clone <repo-url>
cd fuel-route-api
pip install -r requirements.txt
python manage.py runserver
```


## 🎥 Demo
Loom Video : https://www.loom.com/share/f271e48f02e244afa0cdce1e27f21d98
