from app.application.common.validation import (
    fail,
    require_non_negative,
    require_text,
    require_timezone,
)
from app.domain.entities import (
    Collaboration,
    CompensationAgreement,
    CompensationAgreementProduct,
    CompensationProduct,
)
from app.domain.enums import CompensationType


def validate_collaboration(collaboration: Collaboration) -> None:
    if collaboration.production_days is not None and collaboration.production_days <= 0:
        fail("production_days must be greater than zero")
    for field_name in (
        "production_started_at",
        "accepted_at",
        "delivery_deadline",
        "closed_at",
    ):
        require_timezone(getattr(collaboration, field_name), field_name)
    if (
        collaboration.closed_at is not None
        and collaboration.closed_at < collaboration.accepted_at
    ):
        fail("closed_at cannot be before accepted_at")


def validate_compensation_agreement(agreement: CompensationAgreement) -> None:
    require_non_negative(agreement.cash_amount, "cash_amount")
    if (
        agreement.compensation_type
        in {CompensationType.PAYMENT, CompensationType.HYBRID}
        and agreement.cash_amount == 0
    ):
        fail("cash_amount must be greater than zero for payment or hybrid agreements")
    if (
        agreement.compensation_type is CompensationType.PRODUCT
        and agreement.cash_amount != 0
    ):
        fail("cash_amount must be zero for product-only agreements")
    require_timezone(agreement.agreed_at, "agreed_at")


def validate_compensation_product(product: CompensationProduct) -> None:
    require_text(product.name, "name")
    if product.reference_value is not None:
        require_non_negative(product.reference_value, "reference_value")


def validate_compensation_agreement_product(
    item: CompensationAgreementProduct,
) -> None:
    if item.quantity <= 0:
        fail("quantity must be greater than zero")
