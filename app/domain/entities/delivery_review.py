from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.enums import DeliveryReviewDecision


@dataclass(frozen=True, slots=True)
class DeliveryReview:
    delivery_id: UUID
    reviewer_user_id: UUID
    decision: DeliveryReviewDecision
    comments: str | None = None
    reviewed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    delivery_review_id: UUID = field(default_factory=uuid4)
