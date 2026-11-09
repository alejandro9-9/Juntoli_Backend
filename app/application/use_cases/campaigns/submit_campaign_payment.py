from dataclasses import dataclass
from uuid import UUID

from app.application.common.exceptions import (
    ApplicationValidationError,
    ConflictError,
    EntityNotFoundError,
    InvalidStateError,
)
from app.application.ports import Clock, UnitOfWork
from app.application.validation.payments import validate_campaign_payment
from app.domain.entities import CampaignPayment
from app.domain.enums import CampaignPaymentStatus, CompensationType


@dataclass(frozen=True, slots=True)
class SubmitCampaignPaymentCommand:
    campaign_id: UUID
    payment_method_id: UUID
    transaction_number: str
    proof_url: str


class SubmitCampaignPayment:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    def execute(self, command: SubmitCampaignPaymentCommand) -> CampaignPayment:
        if not command.transaction_number.strip():
            raise ApplicationValidationError("transaction_number cannot be empty")
        if not command.proof_url.strip():
            raise ApplicationValidationError("proof_url cannot be empty")

        with self._uow:
            campaign = self._uow.campaigns.get_by_id(command.campaign_id)
            if campaign is None:
                raise EntityNotFoundError("campaign not found")
            if campaign.compensation_type is CompensationType.PRODUCT:
                raise InvalidStateError("product-only campaigns do not require a deposit")
            if self._uow.payment_methods.get_by_id(command.payment_method_id) is None:
                raise EntityNotFoundError("payment method not found")

            previous_payment = self._uow.campaign_payments.get_latest_by_campaign(
                command.campaign_id
            )
            if (
                previous_payment is not None
                and previous_payment.status is not CampaignPaymentStatus.REJECTED
            ):
                raise ConflictError("campaign already has an active or completed deposit")

            now = self._clock.now()
            payment = CampaignPayment(
                campaign_id=campaign.campaign_id,
                payment_method_id=command.payment_method_id,
                amount=campaign.budget,
                currency=campaign.currency,
                status=CampaignPaymentStatus.IN_VALIDATION,
                proof_url=command.proof_url,
                transaction_number=command.transaction_number,
                created_at=now,
                paid_at=now,
            )
            validate_campaign_payment(payment)
            self._uow.campaign_payments.add(payment)
            self._uow.commit()
            return payment
