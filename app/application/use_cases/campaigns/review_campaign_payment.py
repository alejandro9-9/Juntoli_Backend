from dataclasses import dataclass
from uuid import UUID

from app.application.common.exceptions import (
    ApplicationValidationError,
    AuthorizationError,
    EntityNotFoundError,
    InvalidStateError,
)
from app.application.ports import Clock, UnitOfWork
from app.application.validation.payments import validate_campaign_payment
from app.domain.entities import CampaignPayment, CampaignStatusHistory
from app.domain.enums import CampaignPaymentStatus, CampaignStatus


@dataclass(frozen=True, slots=True)
class ReviewCampaignPaymentCommand:
    campaign_payment_id: UUID
    reviewer_user_id: UUID
    approved: bool
    notes: str | None = None


class ReviewCampaignPayment:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    def execute(self, command: ReviewCampaignPaymentCommand) -> CampaignPayment:
        if not command.approved and (command.notes is None or not command.notes.strip()):
            raise ApplicationValidationError("notes are required when a deposit is rejected")

        with self._uow:
            if not self._uow.users.is_admin(command.reviewer_user_id):
                raise AuthorizationError("only an administrator can review deposits")

            payment = self._uow.campaign_payments.get_by_id(command.campaign_payment_id)
            if payment is None:
                raise EntityNotFoundError("campaign payment not found")
            if payment.status is not CampaignPaymentStatus.IN_VALIDATION:
                raise InvalidStateError("campaign payment is not awaiting validation")

            campaign = self._uow.campaigns.get_by_id(payment.campaign_id)
            if campaign is None:
                raise EntityNotFoundError("campaign not found")
            if campaign.status in {CampaignStatus.CANCELLED, CampaignStatus.COMPLETED}:
                raise InvalidStateError("campaign cannot receive a deposit review")

            now = self._clock.now()
            payment.status = (
                CampaignPaymentStatus.VALIDATED
                if command.approved
                else CampaignPaymentStatus.REJECTED
            )
            payment.reviewed_at = now
            payment.reviewed_by_user_id = command.reviewer_user_id
            payment.review_notes = command.notes
            validate_campaign_payment(payment)
            self._uow.campaign_payments.update(payment)

            if command.approved:
                previous_status = campaign.status
                campaign.status = CampaignStatus.APPLICATIONS_OPEN
                campaign.application_start_date = now
                self._uow.campaigns.update(campaign)
                self._uow.campaigns.add_status_history(
                    CampaignStatusHistory(
                        campaign_id=campaign.campaign_id,
                        previous_status=previous_status,
                        new_status=campaign.status,
                        changed_by_user_id=command.reviewer_user_id,
                        changed_at=now,
                    )
                )

            self._uow.commit()
            return payment
