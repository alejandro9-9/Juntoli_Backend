from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from app.domain.enums import CampaignStatus, CompensationType, Currency, Platform


@dataclass(slots=True)
class Campaign:
    brand_id: UUID
    compensation_type: CompensationType
    name: str
    brief: str
    deliverables: str
    platforms: frozenset[Platform]
    budget: Decimal = Decimal("0")
    category_ids: frozenset[UUID] = field(default_factory=frozenset)
    currency: Currency = Currency.PEN
    status: CampaignStatus = CampaignStatus.DRAFT
    application_start_date: datetime | None = None
    application_end_date: datetime | None = None
    delivery_deadline: datetime | None = None
    production_days: int | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    campaign_id: UUID = field(default_factory=uuid4)
