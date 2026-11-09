from dataclasses import dataclass, field
from uuid import UUID, uuid4

@dataclass(slots=True)
class Category:
    name: str
    description: str | None = None
    category_id: UUID = field(default_factory=uuid4)
