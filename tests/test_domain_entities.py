import unittest
from dataclasses import is_dataclass
from decimal import Decimal
from uuid import uuid4

from app.domain.entities import (
    BrandMember,
    Campaign,
    CampaignApplication,
    CampaignPayment,
    CampaignProduct,
    Collaboration,
    CollaborationReview,
    CreatorPayment,
    CreatorPayoutAccount,
    DeliveryReview,
    DisputeMessage,
    ProductShipment,
    Role,
    ShipmentDetail,
    User,
)
from app.domain.enums import (
    BrandResponsibility,
    CompensationType,
    Currency,
    DeliveryReviewDecision,
    Platform,
)


class DomainEntityTests(unittest.TestCase):
    def test_exported_models_are_dataclasses(self) -> None:
        for model in (
            BrandMember,
            Campaign,
            CampaignApplication,
            CampaignPayment,
            CampaignProduct,
            Collaboration,
            CollaborationReview,
            CreatorPayment,
            CreatorPayoutAccount,
            DeliveryReview,
            DisputeMessage,
            ProductShipment,
            Role,
            ShipmentDetail,
            User,
        ):
            self.assertTrue(is_dataclass(model))

    def test_core_entities_generate_uuid_identifiers(self) -> None:
        campaign = Campaign(
            brand_id=uuid4(),
            compensation_type=CompensationType.PAYMENT,
            name="Campaign",
            brief="Campaign brief",
            deliverables="One reel and three stories",
            platforms=frozenset({Platform.INSTAGRAM}),
            budget=Decimal("1000"),
            currency=Currency.PEN,
        )
        collaboration = Collaboration(campaign_application_id=uuid4())
        payment = CampaignPayment(
            campaign_id=campaign.campaign_id,
            payment_method_id=uuid4(),
            amount=Decimal("1000"),
        )
        self.assertIsNotNone(campaign.campaign_id)
        self.assertIsNotNone(collaboration.collaboration_id)
        self.assertIsNotNone(payment.campaign_payment_id)

    def test_creator_payment_net_amount_is_derived(self) -> None:
        payment = CreatorPayment(
            collaboration_id=uuid4(),
            creator_payout_account_id=uuid4(),
            gross_amount=Decimal("100"),
            commission=Decimal("10"),
            tax=Decimal("5"),
        )

        self.assertEqual(payment.net_amount, Decimal("85"))

    def test_new_domain_relationships_keep_their_own_data(self) -> None:
        brand_id = uuid4()
        campaign_id = uuid4()
        creator_id = uuid4()
        payment_method_id = uuid4()
        delivery_id = uuid4()

        member = BrandMember(
            brand_id=brand_id,
            user_id=uuid4(),
            responsibility=BrandResponsibility.FINANCE,
        )
        product = CampaignProduct(
            campaign_id=campaign_id,
            compensation_product_id=uuid4(),
            quantity=2,
        )
        payout_account = CreatorPayoutAccount(
            creator_id=creator_id,
            payment_method_id=payment_method_id,
            account_holder="Creator Name",
            account_reference="encrypted-reference",
            is_default=True,
        )
        delivery_review = DeliveryReview(
            delivery_id=delivery_id,
            reviewer_user_id=member.user_id,
            decision=DeliveryReviewDecision.APPROVED,
        )

        self.assertEqual(member.responsibility, BrandResponsibility.FINANCE)
        self.assertEqual(product.quantity, 2)
        self.assertTrue(payout_account.is_default)
        self.assertEqual(delivery_review.delivery_id, delivery_id)

    def test_dispute_message_references_dispute_directly(self) -> None:
        dispute_id = uuid4()
        message = DisputeMessage(
            dispute_id=dispute_id,
            sender_user_id=uuid4(),
            message="Evidence attached",
        )
        self.assertEqual(message.dispute_id, dispute_id)
        self.assertIsNotNone(message.dispute_message_id)
        self.assertIsNotNone(message.sent_at.tzinfo)


if __name__ == "__main__":
    unittest.main()
