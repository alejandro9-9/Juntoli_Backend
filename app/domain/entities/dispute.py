from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.enums import DisputeStatus, DisputeType


@dataclass(slots=True)
class Dispute:
    collaboration_id: UUID
    reporting_user_id: UUID
    dispute_type: DisputeType
    description: str
    status: DisputeStatus = DisputeStatus.OPEN
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: datetime | None = None
    dispute_id: UUID = field(default_factory=uuid4)
