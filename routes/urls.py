from django.urls import path
from .views import health_check,fuel_data_sample , get_route , fuel_route 

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("fuel-sample/", fuel_data_sample),
    path("route/", get_route),
    path("fuel-route/", fuel_route),
]