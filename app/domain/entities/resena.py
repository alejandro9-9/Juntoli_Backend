from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import IntEnum
from uuid import UUID, uuid4


class Calificacion(IntEnum):
    UNO= 1
    DOS= 2
    TRES= 3
    CUATRO= 4
    CINCO= 5



@dataclass
class Resena : 
    id_colaboracion: UUID
    id_usuario_calificador: UUID
    id_usuario_calificado: UUID
    comentario: str
    calificacion: Calificacion
    creada_en: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    id_resena: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        self.calificacion = Calificacion(self.calificacion)