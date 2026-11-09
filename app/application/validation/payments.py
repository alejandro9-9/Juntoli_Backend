from app.application.common.validation import (
    fail,
    require_non_negative,
    require_text,
    require_timezone,
)
from app.domain.entities import (
    CampaignPayment,
    CreatorPayment,
    CreatorPayoutAccount,
    PaymentMethod,
)
from app.domain.enums import CampaignPaymentStatus, CreatorPaymentStatus


def validate_payment_method(method: PaymentMethod) -> None:
    require_text(method.name, "name")


def validate_campaign_payment(payment: CampaignPayment) -> None:
    if payment.amount <= 0:
        fail("amount must be greater than zero")
    for field_name in ("created_at", "paid_at", "reviewed_at"):
        require_timezone(getattr(payment, field_name), field_name)
    if payment.status in {
        CampaignPaymentStatus.VALIDATED,
        CampaignPaymentStatus.REJECTED,
    }:
        if payment.reviewed_at is None:
            fail("reviewed_at is required for a reviewed payment")
        if payment.reviewed_by_user_id is None:
            fail("reviewed_by_user_id is required for a reviewed payment")


def validate_creator_payment(payment: CreatorPayment) -> None:
    if payment.gross_amount <= 0:
        fail("gross_amount must be greater than zero")
    require_non_negative(payment.commission, "commission")
    require_non_negative(payment.tax, "tax")
    if payment.commission + payment.tax > payment.gross_amount:
        fail("commission plus tax cannot exceed gross_amount")
    require_timezone(payment.created_at, "created_at")
    require_timezone(payment.paid_at, "paid_at")
    if payment.status is CreatorPaymentStatus.PAID and payment.paid_at is None:
        fail("paid_at is required for a paid creator payment")


def validate_creator_payout_account(account: CreatorPayoutAccount) -> None:
    require_text(account.account_holder, "account_holder")
    require_text(account.account_reference, "account_reference")
