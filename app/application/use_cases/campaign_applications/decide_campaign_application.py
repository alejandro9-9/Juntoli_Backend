from dataclasses import dataclass
from uuid import UUID

from app.application.common.exceptions import (
    ApplicationValidationError,
    AuthorizationError,
    EntityNotFoundError,
    InvalidStateError,
)
from app.application.ports import Clock, UnitOfWork
from app.application.validation.campaign_applications import (
    validate_campaign_application,
)
from app.domain.entities import CampaignApplication
from app.domain.enums import CampaignApplicationStatus


@dataclass(frozen=True, slots=True)
class DecideCampaignApplicationCommand:
    campaign_application_id: UUID
    responsible_user_id: UUID
    decision: CampaignApplicationStatus


class DecideCampaignApplication:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    def execute(self, command: DecideCampaignApplicationCommand) -> CampaignApplication:
        if command.decision not in {
            CampaignApplicationStatus.ACCEPTED,
            CampaignApplicationStatus.REJECTED,
        }:
            raise ApplicationValidationError("decision must be accepted or rejected")

        with self._uow:
            application = self._uow.campaign_applications.get_by_id(
                command.campaign_application_id
            )
            if application is None:
                raise EntityNotFoundError("campaign application not found")
            if application.status is not CampaignApplicationStatus.PENDING:
                raise InvalidStateError("campaign application has already been resolved")

            campaign = self._uow.campaigns.get_by_id(application.campaign_id)
            if campaign is None:
                raise EntityNotFoundError("campaign not found")
            if not self._uow.brands.has_active_member(
                campaign.brand_id,
                command.responsible_user_id,
            ):
                raise AuthorizationError("user cannot manage this brand's applications")

            application.status = command.decision
            application.resolved_at = self._clock.now()
            validate_campaign_application(application)
            self._uow.campaign_applications.update(application)
            self._uow.commit()
            return application
