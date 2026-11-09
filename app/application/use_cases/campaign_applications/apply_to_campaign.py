from dataclasses import dataclass
from uuid import UUID

from app.application.common.exceptions import (
    ConflictError,
    EntityNotFoundError,
    InvalidStateError,
)
from app.application.ports import Clock, UnitOfWork
from app.application.validation.campaign_applications import (
    validate_campaign_application,
)
from app.domain.entities import CampaignApplication
from app.domain.enums import CampaignStatus


@dataclass(frozen=True, slots=True)
class ApplyToCampaignCommand:
    campaign_id: UUID
    creator_id: UUID


class ApplyToCampaign:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    def execute(self, command: ApplyToCampaignCommand) -> CampaignApplication:
        with self._uow:
            campaign = self._uow.campaigns.get_by_id(command.campaign_id)
            if campaign is None:
                raise EntityNotFoundError("campaign not found")
            if self._uow.creators.get_by_id(command.creator_id) is None:
                raise EntityNotFoundError("creator not found")
            if campaign.status is not CampaignStatus.APPLICATIONS_OPEN:
                raise InvalidStateError("campaign is not accepting applications")

            now = self._clock.now()
            if (
                campaign.application_start_date is not None
                and now < campaign.application_start_date
            ):
                raise InvalidStateError("campaign applications have not started")
            if (
                campaign.application_end_date is not None
                and now > campaign.application_end_date
            ):
                raise InvalidStateError("campaign applications are closed")
            if self._uow.campaign_applications.get_by_campaign_and_creator(
                command.campaign_id,
                command.creator_id,
            ) is not None:
                raise ConflictError("creator already applied to this campaign")

            application = CampaignApplication(
                campaign_id=command.campaign_id,
                creator_id=command.creator_id,
                applied_at=now,
            )
            validate_campaign_application(application)
            self._uow.campaign_applications.add(application)
            self._uow.commit()
            return application
