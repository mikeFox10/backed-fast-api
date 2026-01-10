from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from app.models.modulo import TipoModulo


class ModuloBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None
    ruta: Optional[str] = Field(None, max_length=255)
    icono: Optional[str] = Field(None, max_length=100)
    tipo: Optional[TipoModulo] = TipoModulo.MENU
    orden: Optional[int] = 0
    is_active: Optional[bool] = True
    parent_id: Optional[int] = None


class ModuloCreate(ModuloBase):
    permiso_ids: Optional[List[int]] = []


class ModuloUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = None
    ruta: Optional[str] = Field(None, max_length=255)
    icono: Optional[str] = Field(None, max_length=100)
    tipo: Optional[TipoModulo] = None
    orden: Optional[int] = None
    is_active: Optional[bool] = None
    parent_id: Optional[int] = None
    permiso_ids: Optional[List[int]] = None


class ModuloResponse(ModuloBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ModuloWithRelations(ModuloResponse):
    permisos: List["PermisoSimple"] = []
    usuarios_count: Optional[int] = 0
    children: List["ModuloResponse"] = []

    model_config = ConfigDict(from_attributes=True)


# Forward reference para evitar problemas de importación circular
from app.schemas.permiso import PermisoSimple
ModuloWithRelations.model_rebuild()
