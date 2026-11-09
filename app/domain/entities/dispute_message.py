from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class DisputeMessage:
    dispute_id: UUID
    sender_user_id: UUID
    message: str
    attachment_url: str | None = None
    sent_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    dispute_message_id: UUID = field(default_factory=uuid4)
