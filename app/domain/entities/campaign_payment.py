from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from app.domain.enums import CampaignPaymentStatus, Currency


@dataclass(slots=True)
class CampaignPayment:
    campaign_id: UUID
    payment_method_id: UUID
    amount: Decimal
    currency: Currency = Currency.PEN
    status: CampaignPaymentStatus = CampaignPaymentStatus.PENDING
    proof_url: str | None = None
    transaction_number: str | None = None
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    paid_at: datetime | None = None
    reviewed_at: datetime | None = None
    reviewed_by_user_id: UUID | None = None
    review_notes: str | None = None
    campaign_payment_id: UUID = field(default_factory=uuid4)
