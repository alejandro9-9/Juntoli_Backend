from app.application.common.validation import fail, require_timezone
from app.domain.entities import CampaignApplication
from app.domain.enums import CampaignApplicationStatus


def validate_campaign_application(application: CampaignApplication) -> None:
    require_timezone(application.applied_at, "applied_at")
    require_timezone(application.resolved_at, "resolved_at")
    if (
        application.status is not CampaignApplicationStatus.PENDING
        and application.resolved_at is None
    ):
        fail("resolved_at is required for a resolved application")
