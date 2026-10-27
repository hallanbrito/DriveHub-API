from rest_framework import serializers
from .models import VehicleModel

class VehicleSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source="brand.name", read_only=True)
    class Meta:
        model = VehicleModel
        fields = ["id", "brand_name", "model", "factory_year", "model_year", "plate", "value", "mileage", "status", "reservation_customer"]

class CreateVehicleSerializer(serializers.Serializer):
    brand_name = serializers.CharField(max_length=200)
    model = serializers.CharField(max_length=200)
    factory_year = serializers.IntegerField()
    model_year = serializers.IntegerField()
    plate = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True, default=None)
    value = serializers.DecimalField(max_digits=12, decimal_places=2)
    mileage = serializers.IntegerField(min_value=0)

class MileageSerializer(serializers.Serializer):
    mileage = serializers.IntegerField(min_value=0)
