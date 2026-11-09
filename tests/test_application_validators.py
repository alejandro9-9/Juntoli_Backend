import unittest
from decimal import Decimal
from uuid import uuid4

from app.application.common.exceptions import ApplicationValidationError
from app.application.use_cases import update_brand_categories
from app.application.validation.campaigns import (
    validate_campaign,
    validate_campaign_product,
)
from app.application.validation.collaborations import validate_compensation_agreement
from app.application.validation.deliveries import validate_delivery_review
from app.application.validation.payments import (
    validate_creator_payment,
    validate_creator_payout_account,
)
from app.application.validation.profiles import validate_brand
from app.application.validation.reviews import validate_collaboration_review
from app.application.validation.shipments import validate_shipment_detail
from app.domain.entities import (
    Brand,
    Campaign,
    CampaignProduct,
    CollaborationReview,
    CompensationAgreement,
    CreatorPayment,
    CreatorPayoutAccount,
    DeliveryReview,
    ShipmentDetail,
)
from app.domain.enums import (
    CompensationType,
    Currency,
    DeliveryReviewDecision,
    Platform,
    Rating,
)


class ApplicationValidatorTests(unittest.TestCase):
    def test_brand_categories_can_be_replaced(self) -> None:
        brand = Brand(name="Brand")
        categories = {uuid4(), uuid4(), uuid4()}

        update_brand_categories(brand, categories)

        self.assertEqual(brand.category_ids, frozenset(categories))
        validate_brand(brand)

    def test_brand_cannot_have_more_than_three_categories(self) -> None:
        brand = Brand(name="Brand")

        with self.assertRaises(ApplicationValidationError):
            update_brand_categories(brand, {uuid4(), uuid4(), uuid4(), uuid4()})

    def test_valid_campaign_is_accepted(self) -> None:
        campaign = Campaign(
            brand_id=uuid4(),
            compensation_type=CompensationType.PAYMENT,
            name="Launch",
            brief="Product launch",
            deliverables="One TikTok video",
            platforms=frozenset({Platform.TIKTOK}),
            budget=Decimal("1500"),
        )
        validate_campaign(campaign)

    def test_campaign_requires_positive_budget(self) -> None:
        campaign = Campaign(
            brand_id=uuid4(),
            compensation_type=CompensationType.PAYMENT,
            name="Launch",
            brief="Product launch",
            deliverables="One TikTok video",
            platforms=frozenset({Platform.TIKTOK}),
            budget=Decimal("0"),
        )
        with self.assertRaises(ApplicationValidationError):
            validate_campaign(campaign)

    def test_creator_payment_deductions_cannot_exceed_gross_amount(self) -> None:
        payment = CreatorPayment(
            collaboration_id=uuid4(),
            creator_payout_account_id=uuid4(),
            gross_amount=Decimal("100"),
            commission=Decimal("70"),
            tax=Decimal("40"),
            currency=Currency.PEN,
        )
        with self.assertRaises(ApplicationValidationError):
            validate_creator_payment(payment)

    def test_user_cannot_review_themselves(self) -> None:
        user_id = uuid4()
        review = CollaborationReview(
            collaboration_id=uuid4(),
            reviewer_user_id=user_id,
            reviewed_user_id=user_id,
            comment="Self review",
            rating=Rating.FIVE,
        )
        with self.assertRaises(ApplicationValidationError):
            validate_collaboration_review(review)

    def test_shipment_detail_requires_positive_quantity(self) -> None:
        detail = ShipmentDetail(
            shipment_id=uuid4(),
            compensation_product_id=uuid4(),
            quantity=0,
        )
        with self.assertRaises(ApplicationValidationError):
            validate_shipment_detail(detail)

    def test_campaign_product_requires_positive_quantity(self) -> None:
        item = CampaignProduct(
            campaign_id=uuid4(),
            compensation_product_id=uuid4(),
            quantity=0,
        )

        with self.assertRaises(ApplicationValidationError):
            validate_campaign_product(item)

    def test_change_request_requires_comments(self) -> None:
        review = DeliveryReview(
            delivery_id=uuid4(),
            reviewer_user_id=uuid4(),
            decision=DeliveryReviewDecision.CHANGES_REQUESTED,
        )

        with self.assertRaises(ApplicationValidationError):
            validate_delivery_review(review)

    def test_creator_payout_account_requires_reference(self) -> None:
        account = CreatorPayoutAccount(
            creator_id=uuid4(),
            payment_method_id=uuid4(),
            account_holder="Creator Name",
            account_reference=" ",
        )

        with self.assertRaises(ApplicationValidationError):
            validate_creator_payout_account(account)

    def test_product_only_campaign_allows_zero_budget(self) -> None:
        campaign = Campaign(
            brand_id=uuid4(),
            compensation_type=CompensationType.PRODUCT,
            name="Product seeding",
            brief="Show the product in use",
            deliverables="One Instagram reel",
            platforms=frozenset({Platform.INSTAGRAM}),
        )

        validate_campaign(campaign)

    def test_product_only_agreement_rejects_cash_amount(self) -> None:
        agreement = CompensationAgreement(
            collaboration_id=uuid4(),
            compensation_type=CompensationType.PRODUCT,
            cash_amount=Decimal("100"),
        )

        with self.assertRaises(ApplicationValidationError):
            validate_compensation_agreement(agreement)


if __name__ == "__main__":
    unittest.main()
