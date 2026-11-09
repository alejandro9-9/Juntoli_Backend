from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.enums import Rating


@dataclass(frozen=True, slots=True)
class CollaborationReview:
    collaboration_id: UUID
    reviewer_user_id: UUID
    reviewed_user_id: UUID
    rating: Rating
    comment: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    collaboration_review_id: UUID = field(default_factory=uuid4)
