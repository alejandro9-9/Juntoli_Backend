from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4


class EstadoUsuario(StrEnum):
    ACTIVO = "activo"
    PENDIENTE = "pendiente"
    SUSPENDIDO = "suspendido"
    ELIMINADO = "eliminado"


@dataclass 
class Usuario:
    id_rol: UUID 
    nombre: str
    email: str
    password_wash: str
    estado: EstadoUsuario
    creado_en: datetime
    is_active: bool = True
    id_usuario: UUID = field(default_factory=uuid4)
    creado_en: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

