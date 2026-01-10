from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional
from datetime import date, datetime
from app.models.persona import Genero


class PersonaBase(BaseModel):
    dni: Optional[str] = Field(None, max_length=20)
    fecha_nacimiento: Optional[date] = None
    genero: Optional[Genero] = None
    telefono: Optional[str] = Field(None, max_length=20)
    telefono_alternativo: Optional[str] = Field(None, max_length=20)
    email_alternativo: Optional[EmailStr] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = Field(None, max_length=100)
    estado_provincia: Optional[str] = Field(None, max_length=100)
    codigo_postal: Optional[str] = Field(None, max_length=20)
    pais: Optional[str] = Field(None, max_length=100)
    foto_perfil: Optional[str] = Field(None, max_length=500)
    biografia: Optional[str] = None
    sitio_web: Optional[str] = Field(None, max_length=255)
    linkedin: Optional[str] = Field(None, max_length=255)
    twitter: Optional[str] = Field(None, max_length=255)
    github: Optional[str] = Field(None, max_length=255)


class PersonaCreate(PersonaBase):
    pass


class PersonaUpdate(BaseModel):
    dni: Optional[str] = Field(None, max_length=20)
    fecha_nacimiento: Optional[date] = None
    genero: Optional[Genero] = None
    telefono: Optional[str] = Field(None, max_length=20)
    telefono_alternativo: Optional[str] = Field(None, max_length=20)
    email_alternativo: Optional[EmailStr] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = Field(None, max_length=100)
    estado_provincia: Optional[str] = Field(None, max_length=100)
    codigo_postal: Optional[str] = Field(None, max_length=20)
    pais: Optional[str] = Field(None, max_length=100)
    foto_perfil: Optional[str] = Field(None, max_length=500)
    biografia: Optional[str] = None
    sitio_web: Optional[str] = Field(None, max_length=255)
    linkedin: Optional[str] = Field(None, max_length=255)
    twitter: Optional[str] = Field(None, max_length=255)
    github: Optional[str] = Field(None, max_length=255)


class PersonaResponse(PersonaBase):
    id: int
    usuario_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
