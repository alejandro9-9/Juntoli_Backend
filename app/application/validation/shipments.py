from app.application.common.validation import fail, require_text, require_timezone
from app.domain.entities import ProductShipment, ShipmentDetail


def validate_product_shipment(shipment: ProductShipment) -> None:
    require_text(shipment.shipping_address, "shipping_address")
    for field_name in (
        "created_at",
        "shipped_at",
        "delivered_at",
        "receipt_confirmed_at",
    ):
        require_timezone(getattr(shipment, field_name), field_name)
    if (
        shipment.shipped_at is not None
        and shipment.delivered_at is not None
        and shipment.delivered_at < shipment.shipped_at
    ):
        fail("delivered_at cannot be before shipped_at")


def validate_shipment_detail(detail: ShipmentDetail) -> None:
    if detail.quantity <= 0:
        fail("quantity must be greater than zero")
