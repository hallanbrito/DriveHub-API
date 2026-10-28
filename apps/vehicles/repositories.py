from core.domain.entities import Brand, Vehicle
from core.domain.enums import VehicleStatus
from .models import BrandModel, VehicleModel

def to_brand(model: BrandModel) -> Brand: return Brand(id=model.id, name=model.name)
def to_vehicle(model: VehicleModel) -> Vehicle:
    return Vehicle(
        id=model.id,
        brand=to_brand(model.brand),
        model=model.model,
        factory_year=model.factory_year,
        model_year=model.model_year,
        plate=model.plate,
        value=model.value,
        mileage=model.mileage,
        status=VehicleStatus(model.status),
        reservation_customer=model.reservation_customer,
        photo_url=model.photo_url,
    )

class DjangoBrandRepository:
    def get_or_create_by_name(self, name: str) -> Brand:
        model, _ = BrandModel.objects.get_or_create(name=name.strip())
        return to_brand(model)

class DjangoVehicleRepository:
    def get_by_id(self, vehicle_id: int) -> Vehicle | None:
        try: model = VehicleModel.objects.select_related("brand").get(pk=vehicle_id)
        except VehicleModel.DoesNotExist: return None
        return to_vehicle(model)
    def save(self, vehicle: Vehicle) -> Vehicle:
        brand_model = BrandModel.objects.get(pk=vehicle.brand.id)
        model, _ = VehicleModel.objects.update_or_create(
            pk=vehicle.id,
            defaults={
                "brand": brand_model, "model": vehicle.model, "factory_year": vehicle.factory_year,
                "model_year": vehicle.model_year, "plate": vehicle.plate, "value": vehicle.value,
                "mileage": vehicle.mileage, "status": vehicle.status.value, "reservation_customer": vehicle.reservation_customer,
                "photo_url": vehicle.photo_url
            }
        )
        return to_vehicle(VehicleModel.objects.select_related("brand").get(pk=model.pk))
