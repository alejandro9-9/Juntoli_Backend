from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.enums import CollaborationStatus


@dataclass(frozen=True, slots=True)
class CollaborationStatusHistory:
    collaboration_id: UUID
    new_status: CollaborationStatus
    previous_status: CollaborationStatus | None = None
    changed_by_user_id: UUID | None = None
    reason: str | None = None
    changed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    collaboration_status_history_id: UUID = field(default_factory=uuid4)
