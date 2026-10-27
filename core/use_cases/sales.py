from decimal import Decimal
from core.domain.entities import SaleProposal
from core.domain.enums import PaymentMethod
from core.domain.exceptions import DomainException
from core.domain.repositories import SaleProposalRepository, VehicleRepository

class CreateSaleProposalUseCase:
    def __init__(self, vehicle_repository: VehicleRepository, proposal_repository: SaleProposalRepository) -> None:
        self.vehicle_repository = vehicle_repository
        self.proposal_repository = proposal_repository
    def execute(self, *, vehicle_id: int, customer_name: str, proposed_value: Decimal, payment_method: PaymentMethod, down_payment: Decimal) -> SaleProposal:
        vehicle = self.vehicle_repository.get_by_id(vehicle_id)
        if vehicle is None:
            raise DomainException("Veículo não encontrado.")
        proposal = SaleProposal.create(vehicle=vehicle, customer_name=customer_name, proposed_value=proposed_value, payment_method=payment_method, down_payment=down_payment)
        self.vehicle_repository.save(vehicle)
        return self.proposal_repository.save(proposal)

class ApproveSaleProposalUseCase:
    def __init__(self, proposal_repository: SaleProposalRepository) -> None:
        self.proposal_repository = proposal_repository
    def execute(self, proposal_id: int) -> SaleProposal:
        proposal = self.proposal_repository.get_by_id(proposal_id)
        if proposal is None:
            raise DomainException("Proposta não encontrada.")
        proposal.approve_by_manager()
        return self.proposal_repository.save(proposal)

class CompleteSaleUseCase:
    def __init__(self, vehicle_repository: VehicleRepository, proposal_repository: SaleProposalRepository) -> None:
        self.vehicle_repository = vehicle_repository
        self.proposal_repository = proposal_repository
    def execute(self, proposal_id: int) -> SaleProposal:
        proposal = self.proposal_repository.get_by_id(proposal_id)
        if proposal is None:
            raise DomainException("Proposta não encontrada.")
        vehicle = self.vehicle_repository.get_by_id(proposal.vehicle_id)
        if vehicle is None:
            raise DomainException("Veículo da proposta não encontrado.")
        proposal.complete(vehicle)
        self.vehicle_repository.save(vehicle)
        return self.proposal_repository.save(proposal)
