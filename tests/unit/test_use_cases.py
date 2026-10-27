from decimal import Decimal
from core.domain.enums import PaymentMethod, ProposalStatus, VehicleStatus
from core.use_cases.sales import ApproveSaleProposalUseCase, CompleteSaleUseCase, CreateSaleProposalUseCase
from core.use_cases.vehicles import CreateVehicleUseCase
from .fakes import InMemoryBrandRepository, InMemorySaleProposalRepository, InMemoryVehicleRepository

def test_complete_sale_flow():
    b, v, p = InMemoryBrandRepository(), InMemoryVehicleRepository(), InMemorySaleProposalRepository()
    veh = CreateVehicleUseCase(b, v).execute(brand_name="Toyota", model="Corolla", factory_year=2023, model_year=2024, value=Decimal("150000.00"), mileage=5000)
    prop = CreateSaleProposalUseCase(v, p).execute(vehicle_id=veh.id, customer_name="Carlos", proposed_value=Decimal("135000.00"), payment_method=PaymentMethod.CASH, down_payment=Decimal("0"))
    app = ApproveSaleProposalUseCase(p).execute(prop.id)
    comp = CompleteSaleUseCase(v, p).execute(app.id)
    assert comp.status == ProposalStatus.COMPLETED
    assert v.get_by_id(veh.id).status == VehicleStatus.SOLD
