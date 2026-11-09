from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.enums import ProductShipmentStatus


@dataclass(slots=True)
class ProductShipment:
    compensation_agreement_id: UUID
    shipping_address: str
    courier_name: str | None = None
    tracking_number: str | None = None
    tracking_url: str | None = None
    status: ProductShipmentStatus = ProductShipmentStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    shipped_at: datetime | None = None
    delivered_at: datetime | None = None
    receipt_confirmed_at: datetime | None = None
    shipment_id: UUID = field(default_factory=uuid4)
