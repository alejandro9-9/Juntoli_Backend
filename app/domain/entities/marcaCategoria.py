from dataclasses import dataclass
from uuid import UUID


@dataclass
class MarcaCategoria:
    id_marca: UUID
    id_categoria: UUID
