from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

class Estado(StrEnum):
    POSTULADO= "postulado"
    RECHAZADO= "rechazado"
    ESCOGIDO= "escogido"

@dataclass
class Postulacion :
    id_campana: UUID
    id_creador: UUID
    estado: Estado
    postulada_en: datetime
    resolvida_en: datetime
    id_postulacion: UUID = field(default_factory= uuid4)
