from typing import Protocol
from uuid import UUID

from app.domain.entities import Creator


class CreatorRepository(Protocol):
    def get_by_id(self, creator_id: UUID) -> Creator | None: ...
