from dataclasses import dataclass , field
from uuid import UUID, uuid4
from datetime import datetime, timezone


@dataclass
class Marca:
    id_usuario: UUID
    nombre: str
    creado_en: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    descripcion: str | None = None
    imagen_perfil_url: str | None = None 
    id_marca: UUID = field(default_factory= uuid4)