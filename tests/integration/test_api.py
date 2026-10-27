import pytest
from rest_framework.test import APIClient
from apps.vehicles.models import VehicleModel

@pytest.mark.django_db
def test_api_vehicle_creation():
    client = APIClient()
    res = client.post("/api/vehicles/vehicles/", {"brand_name": "Fiat", "model": "Pulse", "factory_year": 2024, "model_year": 2025, "value": "100000.00", "mileage": 0}, format="json")
    assert res.status_code == 201
    assert VehicleModel.objects.count() == 1
