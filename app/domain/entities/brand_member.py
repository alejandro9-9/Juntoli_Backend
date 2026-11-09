from dataclasses import dataclass, field
from uuid import UUID, uuid4

from app.domain.enums import BrandResponsibility


@dataclass(slots=True)
class BrandMember:
    brand_id: UUID
    user_id: UUID
    responsibility: BrandResponsibility
    active: bool = True
    brand_member_id: UUID = field(default_factory=uuid4)
