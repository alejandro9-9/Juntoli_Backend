from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.enums import CollaborationStatus


@dataclass(slots=True)
class Collaboration:
    campaign_application_id: UUID
    production_days: int | None = None
    status: CollaborationStatus = CollaborationStatus.CONFIRMED
    production_started_at: datetime | None = None
    accepted_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    delivery_deadline: datetime | None = None
    closed_at: datetime | None = None
    collaboration_id: UUID = field(default_factory=uuid4)

