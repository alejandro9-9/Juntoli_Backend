from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID


class Estado(StrEnum) :
    PENDIENTE = "Pendiente"
    ACEPTADO = "Aceptado"
    RECHAZADO = "Rechazado"
    CANCELADO = "Cancelado"
    
@dataclass 
class AcuerdoCompensacion : 
    id_colaboracion : UUID
    id_modalidad_colaboracion : UUID
    estado: Estado
    acordado_en : datetime
    importe_efectivo : Decimal | None = None