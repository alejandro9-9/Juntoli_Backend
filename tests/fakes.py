from collections import defaultdict
from datetime import datetime
from types import TracebackType
from uuid import UUID

from app.domain.entities import (
    Brand,
    Campaign,
    CampaignApplication,
    CampaignPayment,
    CampaignProduct,
    CampaignStatusHistory,
    Collaboration,
    CollaborationStatusHistory,
    CompensationAgreement,
    CompensationAgreementProduct,
    Creator,
    PaymentMethod,
)


class FixedClock:
    def __init__(self, value: datetime) -> None:
        self.value = value

    def now(self) -> datetime:
        return self.value


class FakeUserRepository:
    def __init__(self) -> None:
        self.admin_ids: set[UUID] = set()

    def is_admin(self, user_id: UUID) -> bool:
        return user_id in self.admin_ids


class FakeBrandRepository:
    def __init__(self) -> None:
        self.items: dict[UUID, Brand] = {}
        self.active_members: set[tuple[UUID, UUID]] = set()

    def get_by_id(self, brand_id: UUID) -> Brand | None:
        return self.items.get(brand_id)

    def has_active_member(self, brand_id: UUID, user_id: UUID) -> bool:
        return (brand_id, user_id) in self.active_members


class FakeCreatorRepository:
    def __init__(self) -> None:
        self.items: dict[UUID, Creator] = {}

    def get_by_id(self, creator_id: UUID) -> Creator | None:
        return self.items.get(creator_id)


class FakePaymentMethodRepository:
    def __init__(self) -> None:
        self.items: dict[UUID, PaymentMethod] = {}

    def get_by_id(self, payment_method_id: UUID) -> PaymentMethod | None:
        return self.items.get(payment_method_id)


class FakeCampaignRepository:
    def __init__(self) -> None:
        self.items: dict[UUID, Campaign] = {}
        self.products: defaultdict[UUID, list[CampaignProduct]] = defaultdict(list)
        self.history: list[CampaignStatusHistory] = []

    def get_by_id(self, campaign_id: UUID) -> Campaign | None:
        return self.items.get(campaign_id)

    def add(self, campaign: Campaign) -> None:
        self.items[campaign.campaign_id] = campaign

    def update(self, campaign: Campaign) -> None:
        self.items[campaign.campaign_id] = campaign

    def add_product(self, product: CampaignProduct) -> None:
        self.products[product.campaign_id].append(product)

    def list_products(self, campaign_id: UUID) -> list[CampaignProduct]:
        return list(self.products[campaign_id])

    def add_status_history(self, history: CampaignStatusHistory) -> None:
        self.history.append(history)


class FakeCampaignApplicationRepository:
    def __init__(self) -> None:
        self.items: dict[UUID, CampaignApplication] = {}

    def get_by_id(self, campaign_application_id: UUID) -> CampaignApplication | None:
        return self.items.get(campaign_application_id)

    def get_by_campaign_and_creator(
        self,
        campaign_id: UUID,
        creator_id: UUID,
    ) -> CampaignApplication | None:
        return next(
            (
                item
                for item in self.items.values()
                if item.campaign_id == campaign_id and item.creator_id == creator_id
            ),
            None,
        )

    def add(self, application: CampaignApplication) -> None:
        self.items[application.campaign_application_id] = application

    def update(self, application: CampaignApplication) -> None:
        self.items[application.campaign_application_id] = application


class FakeCampaignPaymentRepository:
    def __init__(self) -> None:
        self.items: dict[UUID, CampaignPayment] = {}

    def get_by_id(self, campaign_payment_id: UUID) -> CampaignPayment | None:
        return self.items.get(campaign_payment_id)

    def get_latest_by_campaign(self, campaign_id: UUID) -> CampaignPayment | None:
        matches = [item for item in self.items.values() if item.campaign_id == campaign_id]
        return max(matches, key=lambda item: item.created_at) if matches else None

    def add(self, payment: CampaignPayment) -> None:
        self.items[payment.campaign_payment_id] = payment

    def update(self, payment: CampaignPayment) -> None:
        self.items[payment.campaign_payment_id] = payment


class FakeCollaborationRepository:
    def __init__(self) -> None:
        self.items: dict[UUID, Collaboration] = {}
        self.history: list[CollaborationStatusHistory] = []
        self.agreements: dict[UUID, CompensationAgreement] = {}
        self.agreement_products: list[CompensationAgreementProduct] = []

    def get_by_id(self, collaboration_id: UUID) -> Collaboration | None:
        return self.items.get(collaboration_id)

    def get_by_campaign_application(
        self,
        campaign_application_id: UUID,
    ) -> Collaboration | None:
        return next(
            (
                item
                for item in self.items.values()
                if item.campaign_application_id == campaign_application_id
            ),
            None,
        )

    def add(self, collaboration: Collaboration) -> None:
        self.items[collaboration.collaboration_id] = collaboration

    def update(self, collaboration: Collaboration) -> None:
        self.items[collaboration.collaboration_id] = collaboration

    def add_status_history(self, history: CollaborationStatusHistory) -> None:
        self.history.append(history)

    def add_compensation_agreement(self, agreement: CompensationAgreement) -> None:
        self.agreements[agreement.compensation_agreement_id] = agreement

    def add_compensation_product(self, product: CompensationAgreementProduct) -> None:
        self.agreement_products.append(product)


class FakeUnitOfWork:
    def __init__(self) -> None:
        self.users = FakeUserRepository()
        self.brands = FakeBrandRepository()
        self.creators = FakeCreatorRepository()
        self.payment_methods = FakePaymentMethodRepository()
        self.campaigns = FakeCampaignRepository()
        self.campaign_applications = FakeCampaignApplicationRepository()
        self.campaign_payments = FakeCampaignPaymentRepository()
        self.collaborations = FakeCollaborationRepository()
        self.commits = 0
        self.rollbacks = 0

    def __enter__(self) -> "FakeUnitOfWork":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            self.rollback()

    def commit(self) -> None:
        self.commits += 1

    def rollback(self) -> None:
        self.rollbacks += 1
