from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreadorCategoria:
    id_creador: UUID
    id_categoria: UUID
