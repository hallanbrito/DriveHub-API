from django.db import models
class BrandModel(models.Model):
    name = models.CharField(max_length=200, unique=True)
    def __str__(self) -> str: return self.name
class VehicleModel(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Disponível"
        RESERVED = "RESERVED", "Reservado"
        MAINTENANCE = "MAINTENANCE", "Em manutenção"
        SOLD = "SOLD", "Vendido"
    brand = models.ForeignKey(BrandModel, on_delete=models.PROTECT, related_name="vehicles")
    model = models.CharField(max_length=200)
    factory_year = models.PositiveIntegerField()
    model_year = models.PositiveIntegerField()
    plate = models.CharField(max_length=10, unique=True, null=True, blank=True)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    mileage = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    reservation_customer = models.CharField(max_length=200, null=True, blank=True)
    photo_url = models.URLField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
