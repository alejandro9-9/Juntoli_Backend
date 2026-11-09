from app.application.common.validation import (
    fail,
    require_non_negative,
    require_text,
    require_timezone,
)
from app.application.validation.profiles import validate_category_ids
from app.domain.entities import Campaign, CampaignProduct
from app.domain.enums import CompensationType


def validate_campaign(campaign: Campaign) -> None:
    require_text(campaign.name, "name")
    require_text(campaign.brief, "brief")
    require_text(campaign.deliverables, "deliverables")
    require_non_negative(campaign.budget, "budget")
    if (
        campaign.compensation_type
        in {CompensationType.PAYMENT, CompensationType.HYBRID}
        and campaign.budget == 0
    ):
        fail("budget must be greater than zero for payment or hybrid campaigns")
    if campaign.compensation_type is CompensationType.PRODUCT and campaign.budget != 0:
        fail("budget must be zero for product-only campaigns")
    if not campaign.platforms:
        fail("platforms cannot be empty")
    validate_category_ids(campaign.category_ids, "campaign")
    if (
        campaign.application_start_date is not None
        and campaign.application_end_date is not None
        and campaign.application_end_date < campaign.application_start_date
    ):
        fail("application_end_date cannot be before application_start_date")
    if (
        campaign.application_end_date is not None
        and campaign.delivery_deadline is not None
        and campaign.delivery_deadline < campaign.application_end_date
    ):
        fail("delivery_deadline cannot be before application_end_date")
    if campaign.production_days is not None and campaign.production_days <= 0:
        fail("production_days must be greater than zero")
    for field_name in (
        "application_start_date",
        "application_end_date",
        "delivery_deadline",
        "created_at",
    ):
        require_timezone(getattr(campaign, field_name), field_name)


def validate_campaign_product(item: CampaignProduct) -> None:
    if item.quantity <= 0:
        fail("quantity must be greater than zero")
