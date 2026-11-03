from dataclasses import dataclass, field
from uuid import UUID, uuid4

@dataclass
class Categoria:
    nombre: str
    descripcion: str | None = None
    id_categoria: UUID = field(default_factory= uuid4)
