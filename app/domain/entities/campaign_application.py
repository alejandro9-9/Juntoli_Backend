from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.enums import CampaignApplicationStatus


@dataclass(slots=True)
class CampaignApplication:
    campaign_id: UUID
    creator_id: UUID
    status: CampaignApplicationStatus = CampaignApplicationStatus.PENDING
    applied_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: datetime | None = None
    campaign_application_id: UUID = field(default_factory=uuid4)
