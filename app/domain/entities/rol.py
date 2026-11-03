from dataclasses import dataclass, field
from uuid import UUID, uuid4

@dataclass
class Rol:
    nombre: str
    id_rol: UUID = field(default_factory=uuid4)
