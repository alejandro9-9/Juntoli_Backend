from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

class EstadoPago (StrEnum):
    APROBADO = "Aprobado"
    EN_PROGRESO = "En_progreso"
    RECHAZADO = "Rechazado"


class Moneda(StrEnum):
    SOLES = "Soles"
    USD= "USD"


@dataclass
class PagoCampana :
    id_campana : UUID
    id_metodo_pago : UUID
    estado_pago : EstadoPago
    importe : Decimal
    moneda: Moneda
    comprobante_url: str
    creado_en: datetime
    pagado_en: datetime
    validado_en: datetime
    validado_por_user: UUID | None = None
    observacion_validacion: str | None = None
    numero_operacion: str | None = None
   