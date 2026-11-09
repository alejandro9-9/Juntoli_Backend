from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass(slots=True)
class CompensationProduct:
    brand_id: UUID
    name: str
    product_url: str | None = None
    image_url: str | None = None
    reference_value: Decimal | None = None
    description: str | None = None
    active: bool = True
    compensation_product_id: UUID = field(default_factory=uuid4)
