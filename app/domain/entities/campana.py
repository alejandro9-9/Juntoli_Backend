from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4


class Plataformas(StrEnum):
    FACEBOOK= "Facebook"
    INSTAGRAM= "Instagram"
    TIKTOK= "Tiktok"
    YOUTUBE= "Youtube"



@dataclass 
class Campana:
    id_marca: UUID 
    id_modalidad_compensacion: UUID
    nombre: str
    descripcion: str
    plataformas: set[Plataformas]
    presupuesto: float | None 
    moneda: str
    fecha_inicio_postulaciones: datetime 
    fecha_cierre_postulaciones: datetime
    fecha_objetivo_entrega: datetime
    creado_en: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    id_campana: UUID = field(default_factory= uuid4)