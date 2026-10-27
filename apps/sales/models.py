from django.db import models
from apps.vehicles.models import VehicleModel
class SaleProposalModel(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = "CASH", "À vista"
        FINANCED = "FINANCED", "Financiado"
    class Status(models.TextChoices):
        APPROVED = "APPROVED", "Aprovada"
        PENDING_MANAGER = "PENDING_MANAGER", "Pendente de gerente"
        COMPLETED = "COMPLETED", "Concluída"
    vehicle = models.ForeignKey(VehicleModel, on_delete=models.PROTECT, related_name="proposals")
    customer_name = models.CharField(max_length=200)
    proposed_value = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    down_payment = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    requires_manager_approval = models.BooleanField(default=False)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.APPROVED)
    created_at = models.DateTimeField(auto_now_add=True)
