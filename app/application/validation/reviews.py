from app.application.common.validation import fail, require_timezone
from app.domain.entities import CollaborationReview


def validate_collaboration_review(review: CollaborationReview) -> None:
    if review.reviewer_user_id == review.reviewed_user_id:
        fail("a user cannot review themselves")
    require_timezone(review.created_at, "created_at")
