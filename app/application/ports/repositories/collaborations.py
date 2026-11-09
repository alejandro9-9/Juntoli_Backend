from typing import Protocol
from uuid import UUID

from app.domain.entities import (
    Collaboration,
    CollaborationStatusHistory,
    CompensationAgreement,
    CompensationAgreementProduct,
)


class CollaborationRepository(Protocol):
    def get_by_id(self, collaboration_id: UUID) -> Collaboration | None: ...

    def get_by_campaign_application(
        self,
        campaign_application_id: UUID,
    ) -> Collaboration | None: ...

    def add(self, collaboration: Collaboration) -> None: ...

    def update(self, collaboration: Collaboration) -> None: ...

    def add_status_history(self, history: CollaborationStatusHistory) -> None: ...

    def add_compensation_agreement(self, agreement: CompensationAgreement) -> None: ...

    def add_compensation_product(self, product: CompensationAgreementProduct) -> None: ...
