from enum import IntEnum, StrEnum


class Currency(StrEnum):
    PEN = "PEN"
    USD = "USD"


class Platform(StrEnum):
    FACEBOOK = "Facebook"
    INSTAGRAM = "Instagram"
    TIKTOK = "TikTok"
    YOUTUBE = "YouTube"


class UserStatus(StrEnum):
    ACTIVE = "active"
    PENDING = "pending"
    SUSPENDED = "suspended"
    DELETED = "deleted"


class CampaignApplicationStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class CampaignStatus(StrEnum):
    DRAFT = "draft"
    APPLICATIONS_OPEN = "applications_open"
    IN_PRODUCTION = "in_production"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class BrandResponsibility(StrEnum):
    ADMINISTRATION = "administration"
    MARKETING = "marketing"
    FINANCE = "finance"
    CONTENT = "content"


class CollaborationStatus(StrEnum):
    CONFIRMED = "confirmed"
    IN_PRODUCTION = "in_production"
    CONTENT_APPROVED = "content_approved"
    IN_DISPUTE = "in_dispute"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CompensationAgreementStatus(StrEnum):
    ACTIVE = "active"
    CANCELLED = "cancelled"


class CompensationType(StrEnum):
    PAYMENT = "payment"
    PRODUCT = "product"
    HYBRID = "hybrid"


class CampaignPaymentStatus(StrEnum):
    PENDING = "pending"
    IN_VALIDATION = "in_validation"
    VALIDATED = "validated"
    REJECTED = "rejected"
    REFUNDED = "refunded"


class CreatorPaymentStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    PAID = "paid"
    FAILED = "failed"
    CANCELLED = "cancelled"


class DeliveryStatus(StrEnum):
    PENDING_REVIEW = "pending_review"
    CHANGES_REQUESTED = "changes_requested"
    APPROVED = "approved"


class DeliveryReviewDecision(StrEnum):
    CHANGES_REQUESTED = "changes_requested"
    APPROVED = "approved"


class ProductShipmentStatus(StrEnum):
    PENDING = "pending"
    PREPARING = "preparing"
    SHIPPED = "shipped"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    INCIDENT = "incident"
    CANCELLED = "cancelled"


class DisputeType(StrEnum):
    PAYMENT = "payment"
    DELIVERY = "delivery"
    OTHER = "other"


class DisputeStatus(StrEnum):
    OPEN = "open"
    UNDER_REVIEW = "under_review"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Rating(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
