from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ShipmentDetail:
    shipment_id: UUID
    compensation_product_id: UUID
    quantity: int
