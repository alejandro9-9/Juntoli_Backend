from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass
class Creador :
    id_usuario: UUID
    nombre_publico: str
    descripcion: str | None = None
    imagen_perfil_url: str | None = None
    id_creador: UUID = field(default_factory= uuid4)
    creado_en: datetime = field(default_factory=lambda: datetime.now(timezone.utc))