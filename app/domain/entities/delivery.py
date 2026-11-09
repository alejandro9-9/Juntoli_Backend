
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.enums import DeliveryStatus


@dataclass(slots=True)
class Delivery:
    collaboration_id: UUID
    name: str
    delivery_url: str
    version: int = 1
    status: DeliveryStatus = DeliveryStatus.PENDING_REVIEW
    notes: str | None = None
    sent_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    delivery_id: UUID = field(default_factory=uuid4)
