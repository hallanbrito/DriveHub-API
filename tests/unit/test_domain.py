from decimal import Decimal
import pytest
from core.domain.entities import Brand, SaleProposal, Vehicle
from core.domain.enums import PaymentMethod, ProposalStatus
from core.domain.exceptions import DomainException

def make_vehicle(**kwargs) -> Vehicle:
    d = {"id": 1, "brand": Brand(id=1, name="Honda"), "model": "Civic", "factory_year": 2023, "model_year": 2024, "plate": "ABC1D23", "value": Decimal("100000.00"), "mileage": 1000}
    d.update(kwargs)
    return Vehicle(**d)

def test_model_year_validation():
    with pytest.raises(DomainException): make_vehicle(factory_year=2025, model_year=2024)

def test_discount_approval():
    p = SaleProposal.create(vehicle=make_vehicle(), customer_name="Maria", proposed_value=Decimal("95000.00"), payment_method=PaymentMethod.CASH)
    assert p.status == ProposalStatus.APPROVED
