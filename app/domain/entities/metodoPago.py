from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID, uuid4

class Revision(StrEnum):
    MANUAL = "Manual"
    AUTOMATICA = "Automatica"



@dataclass
class MetodoPago:
    nombre: str
    revision: Revision
    activo: bool = True
    id_metodo_pago: UUID = field(default_factory= uuid4)

    def __post_init__(self):
        self.revision = Revision(self.revision)
