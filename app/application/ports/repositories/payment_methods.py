from typing import Protocol
from uuid import UUID

from app.domain.entities import PaymentMethod


class PaymentMethodRepository(Protocol):
    def get_by_id(self, payment_method_id: UUID) -> PaymentMethod | None: ...
