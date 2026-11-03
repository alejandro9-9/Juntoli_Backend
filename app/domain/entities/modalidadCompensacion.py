from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class ModalidadCompensacion:
    nombre: str
    descripcion:str 
    is_active: bool = True
    id_modalidad_compensacion : UUID = field(default_factory= uuid4)
