from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.enums import UserStatus


@dataclass(slots=True)
class User:
    role_id: UUID
    name: str
    email: str
    password_hash: str
    status: UserStatus = UserStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: UUID = field(default_factory=uuid4)

