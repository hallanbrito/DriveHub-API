from decimal import Decimal
from core.domain.entities import Vehicle
from core.domain.enums import VehicleStatus
from core.domain.exceptions import DomainException
from core.domain.repositories import BrandRepository, VehicleRepository

class CreateVehicleUseCase:
    def __init__(self, brand_repository: BrandRepository, vehicle_repository: VehicleRepository) -> None:
        self.brand_repository = brand_repository
        self.vehicle_repository = vehicle_repository

    def execute(self, *, brand_name: str, model: str, factory_year: int, model_year: int, value: Decimal, mileage: int, plate: str | None = None, photo_url: str | None = None) -> Vehicle:
        brand = self.brand_repository.get_or_create_by_name(brand_name)
        vehicle = Vehicle(brand=brand, model=model, factory_year=factory_year, model_year=model_year, plate=plate, value=value, mileage=mileage, status=VehicleStatus.AVAILABLE, photo_url=photo_url)
        return self.vehicle_repository.save(vehicle)

class UpdateVehicleMileageUseCase:
    def __init__(self, vehicle_repository: VehicleRepository) -> None:
        self.vehicle_repository = vehicle_repository

    def execute(self, vehicle_id: int, new_mileage: int) -> Vehicle:
        vehicle = self.vehicle_repository.get_by_id(vehicle_id, for_update=True)
        if vehicle is None:
            raise DomainException("Veículo não encontrado.")
        vehicle.update_mileage(new_mileage)
        return self.vehicle_repository.save(vehicle)
