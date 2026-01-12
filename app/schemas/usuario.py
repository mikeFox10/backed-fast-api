from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional, List
from datetime import datetime


class UsuarioBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    nombre_completo: str = Field(..., min_length=1, max_length=200)
    is_active: Optional[bool] = True
    rol_ids: Optional[List[int]] = []


class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6)


class UsuarioUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    nombre_completo: Optional[str] = Field(None, min_length=1, max_length=200)
    password: Optional[str] = Field(None, min_length=6)
    is_active: Optional[bool] = None
    rol_ids: Optional[List[int]] = None


class RolSimple(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ModuloSimple(BaseModel):
    id: int
    nombre: str
    ruta: Optional[str] = None
    icono: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UsuarioResponse(UsuarioBase):
    id: int
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UsuarioWithRelations(UsuarioResponse):
    roles: List[RolSimple] = []
    modulos: List[ModuloSimple] = []  # Calculados desde roles
    persona: Optional["PersonaResponse"] = None

    model_config = ConfigDict(from_attributes=True)


# Forward reference para evitar problemas de importación circular
from app.schemas.persona import PersonaResponse
UsuarioWithRelations.model_rebuild()


class UsuarioLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UsuarioResponse
