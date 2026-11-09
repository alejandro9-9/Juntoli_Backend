from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(slots=True)
class Role:
    name: str
    role_id: UUID = field(default_factory=uuid4)
