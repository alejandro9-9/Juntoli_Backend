from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(slots=True)
class PaymentMethod:
    name: str
    instructions: str | None = None
    active: bool = True
    payment_method_id: UUID = field(default_factory=uuid4)
