from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from app.domain.enums import CreatorPaymentStatus, Currency


@dataclass(slots=True)
class CreatorPayment:
    collaboration_id: UUID
    creator_payout_account_id: UUID
    gross_amount: Decimal
    commission: Decimal = Decimal("0")
    tax: Decimal = Decimal("0")
    currency: Currency = Currency.PEN
    status: CreatorPaymentStatus = CreatorPaymentStatus.PENDING
    proof_url: str | None = None
    transaction_reference: str | None = None
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    paid_at: datetime | None = None
    creator_payment_id: UUID = field(default_factory=uuid4)

    @property
    def net_amount(self) -> Decimal:
        return self.gross_amount - self.commission - self.tax
