from core.domain.entities import SaleProposal
from core.domain.enums import PaymentMethod, ProposalStatus
from .models import SaleProposalModel

def to_proposal(model: SaleProposalModel) -> SaleProposal:
    return SaleProposal(id=model.id, vehicle_id=model.vehicle_id, customer_name=model.customer_name, proposed_value=model.proposed_value, payment_method=PaymentMethod(model.payment_method), down_payment=model.down_payment, requires_manager_approval=model.requires_manager_approval, status=ProposalStatus(model.status))

class DjangoSaleProposalRepository:
    def get_by_id(self, proposal_id: int) -> SaleProposal | None:
        try: model = SaleProposalModel.objects.get(pk=proposal_id)
        except SaleProposalModel.DoesNotExist: return None
        return to_proposal(model)
    def save(self, proposal: SaleProposal) -> SaleProposal:
        model, _ = SaleProposalModel.objects.update_or_create(
            pk=proposal.id,
            defaults={
                "vehicle_id": proposal.vehicle_id, "customer_name": proposal.customer_name,
                "proposed_value": proposal.proposed_value, "payment_method": proposal.payment_method.value,
                "down_payment": proposal.down_payment, "requires_manager_approval": proposal.requires_manager_approval,
                "status": proposal.status.value
            }
        )
        return to_proposal(SaleProposalModel.objects.get(pk=model.pk))
