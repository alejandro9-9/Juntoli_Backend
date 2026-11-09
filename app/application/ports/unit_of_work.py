from types import TracebackType
from typing import Protocol, Self

from app.application.ports.repositories import (
    BrandRepository,
    CampaignApplicationRepository,
    CampaignPaymentRepository,
    CampaignRepository,
    CollaborationRepository,
    CreatorRepository,
    PaymentMethodRepository,
    UserRepository,
)


class UnitOfWork(Protocol):
    users: UserRepository
    brands: BrandRepository
    creators: CreatorRepository
    payment_methods: PaymentMethodRepository
    campaigns: CampaignRepository
    campaign_applications: CampaignApplicationRepository
    campaign_payments: CampaignPaymentRepository
    collaborations: CollaborationRepository

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...
