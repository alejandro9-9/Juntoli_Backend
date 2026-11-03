from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Colaboracion : 
    id_postulacion: UUID
    dias_produccion: int
    produccion_iniciada: datetime
    aceptada_en: datetime
    fecha_limite_entrega: datetime
    cerrada_en: datetime
     

