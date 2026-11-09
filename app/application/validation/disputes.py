from app.application.common.validation import fail, require_text, require_timezone
from app.domain.entities import Dispute
from app.domain.enums import DisputeStatus


def validate_dispute(dispute: Dispute) -> None:
    require_text(dispute.description, "description")
    require_timezone(dispute.created_at, "created_at")
    require_timezone(dispute.resolved_at, "resolved_at")
    if (
        dispute.status in {DisputeStatus.RESOLVED, DisputeStatus.CLOSED}
        and dispute.resolved_at is None
    ):
        fail("resolved_at is required for a resolved or closed dispute")
