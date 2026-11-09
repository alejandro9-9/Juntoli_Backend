from typing import Protocol
from uuid import UUID

from app.domain.entities import Brand


class BrandRepository(Protocol):
    def get_by_id(self, brand_id: UUID) -> Brand | None: ...

    def has_active_member(self, brand_id: UUID, user_id: UUID) -> bool: ...
