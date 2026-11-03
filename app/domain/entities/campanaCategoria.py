from dataclasses import dataclass
from uuid import UUID


@dataclass
class CampanaCategoria:
    id_campana: UUID
    id_categoria: UUID
