from decimal import Decimal
import pytest
from core.domain.entities import Brand, SaleProposal, Vehicle
from core.domain.enums import PaymentMethod, ProposalStatus, VehicleStatus
from core.domain.exceptions import DomainException

def make_vehicle(**kwargs) -> Vehicle:
    d = {
        "id": 1,
        "brand": Brand(id=1, name="Honda"),
        "model": "Civic",
        "factory_year": 2023,
        "model_year": 2024,
        "plate": "ABC1D23",
        "value": Decimal("100000.00"),
        "mileage": 1000,
    }
    d.update(kwargs)
    return Vehicle(**d)

# Validações de Ano e Quilometragem
def test_model_year_cannot_be_less_than_factory_year():
    with pytest.raises(DomainException, match="O ano do modelo não pode ser menor"):
        make_vehicle(factory_year=2025, model_year=2024)

def test_factory_year_minimum_validation():
    with pytest.raises(DomainException, match="O ano de fabricação é inválido"):
        make_vehicle(factory_year=1885, model_year=1885)

def test_mileage_cannot_be_negative():
    with pytest.raises(DomainException, match="A quilometragem não pode ser negativa"):
        make_vehicle(mileage=-5)

def test_mileage_cannot_be_reduced():
    v = make_vehicle(mileage=15000)
    with pytest.raises(DomainException, match="A quilometragem não pode ser menor"):
        v.update_mileage(14999)

def test_mileage_can_be_increased():
    v = make_vehicle(mileage=15000)
    v.update_mileage(15001)
    assert v.mileage == 15001

# Governança de Descontos
def test_discount_up_to_five_percent_approved_automatically():
    p = SaleProposal.create(
        vehicle=make_vehicle(value=Decimal("100000.00")),
        customer_name="Maria",
        proposed_value=Decimal("95000.00"),  # 5% desconto
        payment_method=PaymentMethod.CASH,
    )
    assert p.status == ProposalStatus.APPROVED
    assert p.requires_manager_approval is False

def test_discount_between_five_and_fifteen_percent_requires_manager():
    p = SaleProposal.create(
        vehicle=make_vehicle(value=Decimal("100000.00")),
        customer_name="Carlos",
        proposed_value=Decimal("90000.00"),  # 10% desconto
        payment_method=PaymentMethod.CASH,
    )
    assert p.status == ProposalStatus.PENDING_MANAGER
    assert p.requires_manager_approval is True

def test_discount_above_fifteen_percent_rejected():
    with pytest.raises(DomainException, match="Descontos acima de 15% não são permitidos"):
        SaleProposal.create(
            vehicle=make_vehicle(value=Decimal("100000.00")),
            customer_name="João",
            proposed_value=Decimal("84000.00"),  # 16% desconto
            payment_method=PaymentMethod.CASH,
        )

# Validações de Financiamento
def test_financed_with_less_than_twenty_percent_down_payment_rejected():
    with pytest.raises(DomainException, match="Financiamento exige entrada mínima de 20%"):
        SaleProposal.create(
            vehicle=make_vehicle(value=Decimal("100000.00")),
            customer_name="Ana",
            proposed_value=Decimal("100000.00"),
            payment_method=PaymentMethod.FINANCED,
            down_payment=Decimal("19999.00"),  # < 20% de 100.000
        )

def test_financed_with_twenty_percent_or_more_down_payment_accepted():
    p = SaleProposal.create(
        vehicle=make_vehicle(value=Decimal("100000.00")),
        customer_name="Ana",
        proposed_value=Decimal("100000.00"),
        payment_method=PaymentMethod.FINANCED,
        down_payment=Decimal("20000.00"),  # exatamente 20%
    )
    assert p.status == ProposalStatus.APPROVED

# Ciclo de Vida e Reservas
def test_vehicle_cannot_be_reserved_by_different_customer():
    v = make_vehicle()
    v.reserve_for("Cliente A")
    assert v.status == VehicleStatus.RESERVED
    with pytest.raises(DomainException, match="O veículo não está disponível para este cliente"):
        v.reserve_for("Cliente B")

def test_sold_vehicle_cannot_receive_proposals_or_be_sold_again():
    v = make_vehicle()
    v.reserve_for("Cliente A")
    v.mark_as_sold("Cliente A")
    assert v.status == VehicleStatus.SOLD
    with pytest.raises(DomainException, match="A venda só pode ser concluída para veículo disponível ou reservado"):
        v.mark_as_sold("Cliente B")
