from enum import StrEnum
class VehicleStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    MAINTENANCE = "MAINTENANCE"
    SOLD = "SOLD"
class PaymentMethod(StrEnum):
    CASH = "CASH"
    FINANCED = "FINANCED"
class ProposalStatus(StrEnum):
    APPROVED = "APPROVED"
    PENDING_MANAGER = "PENDING_MANAGER"
    COMPLETED = "COMPLETED"
