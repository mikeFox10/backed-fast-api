from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.permiso import PermisoSimple


class RolBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None
    is_active: Optional[bool] = True


class RolCreate(RolBase):
    permiso_ids: Optional[List[int]] = []


class RolUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = None
    is_active: Optional[bool] = None
    permiso_ids: Optional[List[int]] = None


class RolResponse(RolBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class RolWithRelations(RolResponse):
    permisos: List[PermisoSimple] = []
    usuarios_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)
