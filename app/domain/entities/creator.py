from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass(slots=True)
class Creator:
    user_id: UUID
    public_name: str
    category_ids: frozenset[UUID] = field(default_factory=frozenset)
    description: str | None = None
    profile_image_url: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    creator_id: UUID = field(default_factory=uuid4)
