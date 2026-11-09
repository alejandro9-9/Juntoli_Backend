from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(slots=True)
class CreatorPayoutAccount:
    creator_id: UUID
    payment_method_id: UUID
    account_holder: str
    account_reference: str
    is_default: bool = False
    active: bool = True
    creator_payout_account_id: UUID = field(default_factory=uuid4)
