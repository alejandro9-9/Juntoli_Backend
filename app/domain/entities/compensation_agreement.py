from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from app.domain.enums import CompensationAgreementStatus, CompensationType, Currency


@dataclass(slots=True)
class CompensationAgreement:
    collaboration_id: UUID
    compensation_type: CompensationType
    cash_amount: Decimal = Decimal("0")
    currency: Currency = Currency.PEN
    status: CompensationAgreementStatus = CompensationAgreementStatus.ACTIVE
    agreed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    compensation_agreement_id: UUID = field(default_factory=uuid4)
