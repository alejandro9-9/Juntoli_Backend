from typing import Protocol
from uuid import UUID


class UserRepository(Protocol):
    def is_admin(self, user_id: UUID) -> bool: ...
