from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime


class PermisoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    codigo: str = Field(..., min_length=1, max_length=50, pattern="^[a-z0-9._]+$")
    descripcion: Optional[str] = None
    is_active: Optional[bool] = True


class PermisoCreate(PermisoBase):
    pass


class PermisoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    codigo: Optional[str] = Field(None, min_length=1, max_length=50, pattern="^[a-z0-9._]+$")
    descripcion: Optional[str] = None
    is_active: Optional[bool] = None


class PermisoResponse(PermisoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PermisoSimple(BaseModel):
    id: int
    nombre: str
    codigo: str

    model_config = ConfigDict(from_attributes=True)


class PermisoWithRelations(PermisoResponse):
    roles_count: Optional[int] = 0
    modulos_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)
