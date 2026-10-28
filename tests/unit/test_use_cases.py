from decimal import Decimal
import pytest
from core.domain.enums import PaymentMethod, ProposalStatus, VehicleStatus
from core.domain.exceptions import DomainException
from core.use_cases.sales import ApproveSaleProposalUseCase, CompleteSaleUseCase, CreateSaleProposalUseCase
from core.use_cases.vehicles import CreateVehicleUseCase, UpdateVehicleMileageUseCase
from .fakes import InMemoryBrandRepository, InMemorySaleProposalRepository, InMemoryVehicleRepository

def test_complete_sale_flow():
    b, v, p = InMemoryBrandRepository(), InMemoryVehicleRepository(), InMemorySaleProposalRepository()
    veh = CreateVehicleUseCase(b, v).execute(
        brand_name="Toyota",
        model="Corolla",
        factory_year=2023,
        model_year=2024,
        value=Decimal("150000.00"),
        mileage=5000,
    )
    # Proposta com 10% desconto (requer gerente)
    prop = CreateSaleProposalUseCase(v, p).execute(
        vehicle_id=veh.id,
        customer_name="Carlos",
        proposed_value=Decimal("135000.00"),
        payment_method=PaymentMethod.CASH,
        down_payment=Decimal("0"),
    )
    assert prop.status == ProposalStatus.PENDING_MANAGER
    assert v.get_by_id(veh.id).status == VehicleStatus.RESERVED

    # Gerente aprova
    app = ApproveSaleProposalUseCase(p, v).execute(prop.id)
    assert app.status == ProposalStatus.APPROVED

    # Conclusão da venda
    comp = CompleteSaleUseCase(v, p).execute(app.id)
    assert comp.status == ProposalStatus.COMPLETED
    assert v.get_by_id(veh.id).status == VehicleStatus.SOLD

def test_cannot_create_proposal_for_vehicle_reserved_by_another_customer():
    b, v, p = InMemoryBrandRepository(), InMemoryVehicleRepository(), InMemorySaleProposalRepository()
    veh = CreateVehicleUseCase(b, v).execute(
        brand_name="Honda",
        model="Civic",
        factory_year=2023,
        model_year=2024,
        value=Decimal("100000.00"),
        mileage=1000,
    )
    # Cliente 1 reserva o veículo
    CreateSaleProposalUseCase(v, p).execute(
        vehicle_id=veh.id,
        customer_name="Cliente 1",
        proposed_value=Decimal("95000.00"),
        payment_method=PaymentMethod.CASH,
        down_payment=Decimal("0"),
    )

    # Cliente 2 tenta criar proposta concorrente no mesmo veículo
    with pytest.raises(DomainException, match="disponível ou reservado ao mesmo cliente"):
        CreateSaleProposalUseCase(v, p).execute(
            vehicle_id=veh.id,
            customer_name="Cliente 2",
            proposed_value=Decimal("95000.00"),
            payment_method=PaymentMethod.CASH,
            down_payment=Decimal("0"),
        )

def test_cannot_complete_sale_without_manager_approval():
    b, v, p = InMemoryBrandRepository(), InMemoryVehicleRepository(), InMemorySaleProposalRepository()
    veh = CreateVehicleUseCase(b, v).execute(
        brand_name="Audi",
        model="A3",
        factory_year=2024,
        model_year=2024,
        value=Decimal("200000.00"),
        mileage=500,
    )
    # Proposta com 10% de desconto -> PENDING_MANAGER
    prop = CreateSaleProposalUseCase(v, p).execute(
        vehicle_id=veh.id,
        customer_name="Roberto",
        proposed_value=Decimal("180000.00"),
        payment_method=PaymentMethod.CASH,
        down_payment=Decimal("0"),
    )
    with pytest.raises(DomainException, match="precisa estar aprovada antes da conclusão"):
        CompleteSaleUseCase(v, p).execute(prop.id)

def test_update_mileage_use_case():
    b, v = InMemoryBrandRepository(), InMemoryVehicleRepository()
    veh = CreateVehicleUseCase(b, v).execute(
        brand_name="BMW",
        model="320i",
        factory_year=2024,
        model_year=2024,
        value=Decimal("300000.00"),
        mileage=1000,
    )
    updated = UpdateVehicleMileageUseCase(v).execute(veh.id, 1500)
    assert updated.mileage == 1500

    # Redução de hodômetro rejeitada
    with pytest.raises(DomainException, match="A quilometragem não pode ser menor"):
        UpdateVehicleMileageUseCase(v).execute(veh.id, 1400)
