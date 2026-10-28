from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from .enums import PaymentMethod, ProposalStatus, VehicleStatus
from .exceptions import DomainException

ZERO = Decimal("0")
FIVE_PERCENT = Decimal("0.05")
FIFTEEN_PERCENT = Decimal("0.15")
TWENTY_PERCENT = Decimal("0.20")

@dataclass
class Brand:
    name: str
    id: Optional[int] = None
    def __post_init__(self) -> None:
        self.name = self.name.strip()
        if not self.name:
            raise DomainException("O nome da marca é obrigatório.")

@dataclass
class Vehicle:
    brand: Brand
    model: str
    factory_year: int
    model_year: int
    plate: Optional[str]
    value: Decimal
    mileage: int
    status: VehicleStatus = VehicleStatus.AVAILABLE
    reservation_customer: Optional[str] = None
    photo_url: Optional[str] = None
    id: Optional[int] = None
    def __post_init__(self) -> None:
        self.model = self.model.strip()
        self.plate = self.plate.strip().upper() if self.plate else None
        self.value = Decimal(str(self.value))
        self.validate()
    def validate(self) -> None:
        if not self.model:
            raise DomainException("O modelo do veículo é obrigatório.")
        if self.factory_year < 1886:
            raise DomainException("O ano de fabricação é inválido.")
        if self.model_year < self.factory_year:
            raise DomainException("O ano do modelo não pode ser menor que o ano de fabricação.")
        if self.value <= ZERO:
            raise DomainException("O valor do veículo deve ser positivo.")
        if self.mileage < 0:
            raise DomainException("A quilometragem não pode ser negativa.")
    def update_mileage(self, new_mileage: int) -> None:
        if new_mileage < self.mileage:
            raise DomainException("A quilometragem não pode ser menor que a quilometragem atual.")
        self.mileage = new_mileage
    def reserve_for(self, customer_name: str) -> None:
        customer_name = customer_name.strip()
        if not customer_name:
            raise DomainException("O nome do cliente é obrigatório.")
        if self.status == VehicleStatus.AVAILABLE:
            self.status = VehicleStatus.RESERVED
            self.reservation_customer = customer_name
            return
        if self.status == VehicleStatus.RESERVED and self.reservation_customer == customer_name:
            return
        raise DomainException("O veículo não está disponível para este cliente.")
    def can_receive_proposal_from(self, customer_name: str) -> bool:
        return self.status == VehicleStatus.AVAILABLE or (self.status == VehicleStatus.RESERVED and self.reservation_customer == customer_name)
    def mark_as_sold(self, customer_name: str) -> None:
        if not self.can_receive_proposal_from(customer_name):
            raise DomainException("A venda só pode ser concluída para veículo disponível ou reservado ao mesmo cliente.")
        self.status = VehicleStatus.SOLD
        self.reservation_customer = customer_name

@dataclass
class SaleProposal:
    vehicle_id: int
    customer_name: str
    proposed_value: Decimal
    payment_method: PaymentMethod
    down_payment: Decimal = ZERO
    id: Optional[int] = None
    status: ProposalStatus = ProposalStatus.APPROVED
    requires_manager_approval: bool = False
    def __post_init__(self) -> None:
        self.customer_name = self.customer_name.strip()
        self.proposed_value = Decimal(str(self.proposed_value))
        self.down_payment = Decimal(str(self.down_payment))
        if not self.customer_name:
            raise DomainException("O nome do cliente é obrigatório.")
        if self.proposed_value <= ZERO:
            raise DomainException("O valor proposto deve ser positivo.")
        if self.down_payment < ZERO:
            raise DomainException("A entrada não pode ser negativa.")
    @classmethod
    def create(cls, vehicle: Vehicle, customer_name: str, proposed_value: Decimal, payment_method: PaymentMethod, down_payment: Decimal = ZERO) -> "SaleProposal":
        if not vehicle.can_receive_proposal_from(customer_name):
            raise DomainException("Propostas só podem ser feitas para veículo disponível ou reservado ao mesmo cliente.")
        proposal = cls(vehicle_id=vehicle.id or 0, customer_name=customer_name, proposed_value=proposed_value, payment_method=payment_method, down_payment=down_payment)
        discount = (vehicle.value - proposal.proposed_value) / vehicle.value
        if discount > FIFTEEN_PERCENT:
            raise DomainException("Descontos acima de 15% não são permitidos.")
        if discount > FIVE_PERCENT:
            proposal.requires_manager_approval = True
            proposal.status = ProposalStatus.PENDING_MANAGER
        if proposal.payment_method == PaymentMethod.FINANCED:
            minimum_down_payment = proposal.proposed_value * TWENTY_PERCENT
            if proposal.down_payment < minimum_down_payment:
                raise DomainException("Financiamento exige entrada mínima de 20% do valor proposto.")
        vehicle.reserve_for(customer_name)
        return proposal
    def approve_by_manager(self) -> None:
        if not self.requires_manager_approval:
            raise DomainException("Esta proposta não requer aprovação gerencial.")
        if self.status != ProposalStatus.PENDING_MANAGER:
            raise DomainException("A proposta não está pendente de aprovação.")
        self.status = ProposalStatus.APPROVED
    def complete(self, vehicle: Vehicle) -> None:
        if self.status != ProposalStatus.APPROVED:
            raise DomainException("A proposta precisa estar aprovada antes da conclusão.")
        vehicle.mark_as_sold(self.customer_name)
        self.status = ProposalStatus.COMPLETED
