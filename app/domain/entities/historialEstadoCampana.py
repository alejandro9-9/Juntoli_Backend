from dataclasses import dataclass, field
from datetime import datetime, timezone 
from enum import StrEnum
from uuid import UUID, uuid4


class EstadoCampana(StrEnum):
    BORRADOR = "borrador"
    PROXIMAMENTE = "proximamente"
    POSTULACIONES = "postulaciones"
    GENERACION_CONTENIDO = "generacion_contenido"
    APROBACION_CONTENIDO= "aprobacion_contenido"
    DISPUTA = "disputa"
    PROCESO_PAGO= "proceso_pago"
    TERMINADO = "terminado"



@dataclass
class HistorialEstadoCampana:
    id_campana: UUID
    estado_nuevo : EstadoCampana 
    cambiado_por : UUID
    fecha_cambio: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    id_historial_estado_campana  : UUID = field(default_factory= uuid4)
    estado_anterior : EstadoCampana | None = None


