from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from app.application.common.exceptions import (
    AuthorizationError,
    ConflictError,
    EntityNotFoundError,
    InvalidStateError,
)
from app.application.ports import Clock, UnitOfWork
from app.application.validation.collaborations import (
    validate_collaboration,
    validate_compensation_agreement,
    validate_compensation_agreement_product,
)
from app.domain.entities import (
    CampaignStatusHistory,
    Collaboration,
    CollaborationStatusHistory,
    CompensationAgreement,
    CompensationAgreementProduct,
)
from app.domain.enums import (
    CampaignApplicationStatus,
    CampaignStatus,
    CollaborationStatus,
)


@dataclass(frozen=True, slots=True)
class StartCollaborationCommand:
    campaign_application_id: UUID
    responsible_user_id: UUID
    cash_amount: Decimal = Decimal("0")


class StartCollaboration:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    def execute(self, command: StartCollaborationCommand) -> Collaboration:
        with self._uow:
            application = self._uow.campaign_applications.get_by_id(
                command.campaign_application_id
            )
            if application is None:
                raise EntityNotFoundError("campaign application not found")
            if application.status is not CampaignApplicationStatus.ACCEPTED:
                raise InvalidStateError("only accepted applications can start collaborations")
            if self._uow.collaborations.get_by_campaign_application(
                application.campaign_application_id
            ) is not None:
                raise ConflictError("application already has a collaboration")

            campaign = self._uow.campaigns.get_by_id(application.campaign_id)
            if campaign is None:
                raise EntityNotFoundError("campaign not found")
            if campaign.status not in {
                CampaignStatus.APPLICATIONS_OPEN,
                CampaignStatus.IN_PRODUCTION,
            }:
                raise InvalidStateError("campaign cannot start collaborations")
            if not self._uow.brands.has_active_member(
                campaign.brand_id,
                command.responsible_user_id,
            ):
                raise AuthorizationError("user cannot manage this brand's collaborations")

            products = self._uow.campaigns.list_products(campaign.campaign_id)
            now = self._clock.now()
            collaboration = Collaboration(
                campaign_application_id=application.campaign_application_id,
                production_days=campaign.production_days,
                status=(
                    CollaborationStatus.CONFIRMED
                    if products
                    else CollaborationStatus.IN_PRODUCTION
                ),
                production_started_at=None if products else now,
                accepted_at=now,
                delivery_deadline=None if products else campaign.delivery_deadline,
            )
            validate_collaboration(collaboration)
            self._uow.collaborations.add(collaboration)
            self._uow.collaborations.add_status_history(
                CollaborationStatusHistory(
                    collaboration_id=collaboration.collaboration_id,
                    new_status=collaboration.status,
                    changed_by_user_id=command.responsible_user_id,
                    changed_at=now,
                )
            )

            agreement = CompensationAgreement(
                collaboration_id=collaboration.collaboration_id,
                compensation_type=campaign.compensation_type,
                cash_amount=command.cash_amount,
                currency=campaign.currency,
                agreed_at=now,
            )
            validate_compensation_agreement(agreement)
            self._uow.collaborations.add_compensation_agreement(agreement)

            for campaign_product in products:
                agreement_product = CompensationAgreementProduct(
                    compensation_agreement_id=agreement.compensation_agreement_id,
                    compensation_product_id=campaign_product.compensation_product_id,
                    quantity=campaign_product.quantity,
                )
                validate_compensation_agreement_product(agreement_product)
                self._uow.collaborations.add_compensation_product(agreement_product)

            if campaign.status is CampaignStatus.APPLICATIONS_OPEN:
                previous_status = campaign.status
                campaign.status = CampaignStatus.IN_PRODUCTION
                self._uow.campaigns.update(campaign)
                self._uow.campaigns.add_status_history(
                    CampaignStatusHistory(
                        campaign_id=campaign.campaign_id,
                        previous_status=previous_status,
                        new_status=campaign.status,
                        changed_by_user_id=command.responsible_user_id,
                        changed_at=now,
                    )
                )

            self._uow.commit()
            return collaboration
