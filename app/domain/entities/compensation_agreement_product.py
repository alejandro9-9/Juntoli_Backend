from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CompensationAgreementProduct:
    compensation_agreement_id: UUID
    compensation_product_id: UUID
    quantity: int
