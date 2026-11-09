from typing import Protocol
from uuid import UUID

from app.domain.entities import CampaignPayment


class CampaignPaymentRepository(Protocol):
    def get_by_id(self, campaign_payment_id: UUID) -> CampaignPayment | None: ...

    def get_latest_by_campaign(self, campaign_id: UUID) -> CampaignPayment | None: ...

    def add(self, payment: CampaignPayment) -> None: ...

    def update(self, payment: CampaignPayment) -> None: ...
