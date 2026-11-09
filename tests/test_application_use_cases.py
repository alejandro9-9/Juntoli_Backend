import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import uuid4

from app.application.use_cases import (
    ApplyToCampaign,
    ApplyToCampaignCommand,
    CampaignProductInput,
    CreateCampaign,
    CreateCampaignCommand,
    DecideCampaignApplication,
    DecideCampaignApplicationCommand,
    ReviewCampaignPayment,
    ReviewCampaignPaymentCommand,
    StartCollaboration,
    StartCollaborationCommand,
    SubmitCampaignPayment,
    SubmitCampaignPaymentCommand,
)
from app.domain.entities import Brand, Campaign, Creator, PaymentMethod
from app.domain.enums import (
    CampaignApplicationStatus,
    CampaignPaymentStatus,
    CampaignStatus,
    CollaborationStatus,
    CompensationType,
    Platform,
)
from tests.fakes import FakeUnitOfWork, FixedClock


class ApplicationUseCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime(2026, 11, 6, 15, 0, tzinfo=timezone.utc)
        self.clock = FixedClock(self.now)
        self.uow = FakeUnitOfWork()

    def test_create_product_campaign_persists_its_products(self) -> None:
        brand = Brand(name="Verde Vivo")
        self.uow.brands.items[brand.brand_id] = brand
        product_id = uuid4()

        campaign = CreateCampaign(self.uow, self.clock).execute(
            CreateCampaignCommand(
                brand_id=brand.brand_id,
                compensation_type=CompensationType.PRODUCT,
                name="Product seeding",
                brief="Show the product in use",
                deliverables="One Instagram reel",
                platforms=frozenset({Platform.INSTAGRAM}),
                application_end_date=self.now + timedelta(days=7),
                production_days=5,
                products=(CampaignProductInput(product_id, 1),),
            )
        )

        self.assertEqual(campaign.status, CampaignStatus.DRAFT)
        self.assertEqual(self.uow.campaigns.products[campaign.campaign_id][0].quantity, 1)
        self.assertEqual(self.uow.commits, 1)

    def test_validated_deposit_opens_campaign_applications(self) -> None:
        brand = Brand(name="Verde Vivo")
        campaign = Campaign(
            brand_id=brand.brand_id,
            compensation_type=CompensationType.PAYMENT,
            name="Launch",
            brief="Launch brief",
            deliverables="One video",
            platforms=frozenset({Platform.TIKTOK}),
            budget=Decimal("1000"),
            application_end_date=self.now + timedelta(days=7),
            delivery_deadline=self.now + timedelta(days=20),
        )
        payment_method = PaymentMethod(name="BBVA transfer")
        admin_id = uuid4()
        self.uow.brands.items[brand.brand_id] = brand
        self.uow.campaigns.items[campaign.campaign_id] = campaign
        self.uow.payment_methods.items[payment_method.payment_method_id] = payment_method
        self.uow.users.admin_ids.add(admin_id)

        payment = SubmitCampaignPayment(self.uow, self.clock).execute(
            SubmitCampaignPaymentCommand(
                campaign_id=campaign.campaign_id,
                payment_method_id=payment_method.payment_method_id,
                transaction_number="OP-123",
                proof_url="https://storage.example/proof.pdf",
            )
        )
        ReviewCampaignPayment(self.uow, self.clock).execute(
            ReviewCampaignPaymentCommand(
                campaign_payment_id=payment.campaign_payment_id,
                reviewer_user_id=admin_id,
                approved=True,
            )
        )

        self.assertEqual(payment.status, CampaignPaymentStatus.VALIDATED)
        self.assertEqual(campaign.status, CampaignStatus.APPLICATIONS_OPEN)
        self.assertEqual(campaign.application_start_date, self.now)

    def test_accepted_application_becomes_collaboration(self) -> None:
        brand = Brand(name="Verde Vivo")
        creator = Creator(user_id=uuid4(), public_name="Maria")
        responsible_user_id = uuid4()
        campaign = Campaign(
            brand_id=brand.brand_id,
            compensation_type=CompensationType.PAYMENT,
            name="Launch",
            brief="Launch brief",
            deliverables="One reel",
            platforms=frozenset({Platform.INSTAGRAM}),
            budget=Decimal("1000"),
            status=CampaignStatus.APPLICATIONS_OPEN,
            application_start_date=self.now - timedelta(days=1),
            application_end_date=self.now + timedelta(days=7),
            delivery_deadline=self.now + timedelta(days=20),
        )
        self.uow.brands.items[brand.brand_id] = brand
        self.uow.brands.active_members.add((brand.brand_id, responsible_user_id))
        self.uow.creators.items[creator.creator_id] = creator
        self.uow.campaigns.items[campaign.campaign_id] = campaign

        application = ApplyToCampaign(self.uow, self.clock).execute(
            ApplyToCampaignCommand(campaign.campaign_id, creator.creator_id)
        )
        DecideCampaignApplication(self.uow, self.clock).execute(
            DecideCampaignApplicationCommand(
                campaign_application_id=application.campaign_application_id,
                responsible_user_id=responsible_user_id,
                decision=CampaignApplicationStatus.ACCEPTED,
            )
        )
        collaboration = StartCollaboration(self.uow, self.clock).execute(
            StartCollaborationCommand(
                campaign_application_id=application.campaign_application_id,
                responsible_user_id=responsible_user_id,
                cash_amount=Decimal("500"),
            )
        )

        self.assertEqual(collaboration.status, CollaborationStatus.IN_PRODUCTION)
        self.assertEqual(collaboration.delivery_deadline, campaign.delivery_deadline)
        self.assertEqual(campaign.status, CampaignStatus.IN_PRODUCTION)
        self.assertEqual(len(self.uow.collaborations.agreements), 1)


if __name__ == "__main__":
    unittest.main()
