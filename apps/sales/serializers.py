from rest_framework import serializers
from .models import SaleProposalModel

class SaleProposalSerializer(serializers.ModelSerializer):
    vehicle_model = serializers.CharField(source="vehicle.model", read_only=True)
    vehicle_plate = serializers.CharField(source="vehicle.plate", read_only=True)
    class Meta:
        model = SaleProposalModel
        fields = ["id", "vehicle", "vehicle_model", "vehicle_plate", "customer_name", "proposed_value", "payment_method", "down_payment", "requires_manager_approval", "status"]

class CreateSaleProposalSerializer(serializers.Serializer):
    vehicle_id = serializers.IntegerField(min_value=1)
    customer_name = serializers.CharField(max_length=200)
    proposed_value = serializers.DecimalField(max_digits=12, decimal_places=2)
    payment_method = serializers.ChoiceField(choices=SaleProposalModel.PaymentMethod.choices)
    down_payment = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, default="0.00")
