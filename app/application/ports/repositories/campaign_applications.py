from typing import Protocol
from uuid import UUID

from app.domain.entities import CampaignApplication


class CampaignApplicationRepository(Protocol):
    def get_by_id(self, campaign_application_id: UUID) -> CampaignApplication | None: ...

    def get_by_campaign_and_creator(
        self,
        campaign_id: UUID,
        creator_id: UUID,
    ) -> CampaignApplication | None: ...

    def add(self, application: CampaignApplication) -> None: ...

    def update(self, application: CampaignApplication) -> None: ...
