from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from app.application.common.exceptions import (
    ApplicationValidationError,
    EntityNotFoundError,
)
from app.application.ports import Clock, UnitOfWork
from app.application.validation.campaigns import (
    validate_campaign,
    validate_campaign_product,
)
from app.domain.entities import Campaign, CampaignProduct
from app.domain.enums import CompensationType, Currency, Platform


@dataclass(frozen=True, slots=True)
class CampaignProductInput:
    compensation_product_id: UUID
    quantity: int


@dataclass(frozen=True, slots=True)
class CreateCampaignCommand:
    brand_id: UUID
    compensation_type: CompensationType
    name: str
    brief: str
    deliverables: str
    platforms: frozenset[Platform]
    application_end_date: datetime
    budget: Decimal = Decimal("0")
    currency: Currency = Currency.PEN
    category_ids: frozenset[UUID] = frozenset()
    delivery_deadline: datetime | None = None
    production_days: int | None = None
    products: tuple[CampaignProductInput, ...] = ()


class CreateCampaign:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    def execute(self, command: CreateCampaignCommand) -> Campaign:
        now = self._clock.now()
        product_compensation = command.compensation_type in {
            CompensationType.PRODUCT,
            CompensationType.HYBRID,
        }

        if command.application_end_date <= now:
            raise ApplicationValidationError("application_end_date must be in the future")
        if product_compensation and not command.products:
            raise ApplicationValidationError(
                "product or hybrid campaigns require at least one product"
            )
        if not product_compensation and command.products:
            raise ApplicationValidationError("payment-only campaigns cannot include products")
        if product_compensation:
            if command.production_days is None:
                raise ApplicationValidationError(
                    "production_days is required when products are shipped"
                )
            if command.delivery_deadline is not None:
                raise ApplicationValidationError(
                    "delivery_deadline must be omitted when production starts after receipt"
                )
        elif command.delivery_deadline is None:
            raise ApplicationValidationError(
                "delivery_deadline is required for campaigns without product shipment"
            )
        elif command.production_days is not None:
            raise ApplicationValidationError(
                "production_days must be omitted when there is no product shipment"
            )

        product_ids = [item.compensation_product_id for item in command.products]
        if len(product_ids) != len(set(product_ids)):
            raise ApplicationValidationError("campaign products cannot be duplicated")

        with self._uow:
            if self._uow.brands.get_by_id(command.brand_id) is None:
                raise EntityNotFoundError("brand not found")

            campaign = Campaign(
                brand_id=command.brand_id,
                compensation_type=command.compensation_type,
                name=command.name,
                brief=command.brief,
                deliverables=command.deliverables,
                platforms=command.platforms,
                budget=command.budget,
                category_ids=command.category_ids,
                currency=command.currency,
                application_end_date=command.application_end_date,
                delivery_deadline=command.delivery_deadline,
                production_days=command.production_days,
                created_at=now,
            )
            validate_campaign(campaign)
            self._uow.campaigns.add(campaign)

            for item in command.products:
                campaign_product = CampaignProduct(
                    campaign_id=campaign.campaign_id,
                    compensation_product_id=item.compensation_product_id,
                    quantity=item.quantity,
                )
                validate_campaign_product(campaign_product)
                self._uow.campaigns.add_product(campaign_product)

            self._uow.commit()
            return campaign
