from app.application.common.validation import fail, require_text, require_timezone
from app.domain.entities import Delivery, DeliveryReview
from app.domain.enums import DeliveryReviewDecision


def validate_delivery(delivery: Delivery) -> None:
    require_text(delivery.name, "name")
    require_text(delivery.delivery_url, "delivery_url")
    if delivery.version <= 0:
        fail("version must be greater than zero")
    require_timezone(delivery.sent_at, "sent_at")


def validate_delivery_review(review: DeliveryReview) -> None:
    require_timezone(review.reviewed_at, "reviewed_at")
    if (
        review.decision is DeliveryReviewDecision.CHANGES_REQUESTED
        and (review.comments is None or not review.comments.strip())
    ):
        fail("comments are required when changes are requested")
