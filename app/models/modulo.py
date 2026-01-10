from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class TipoModulo(str, enum.Enum):
    MENU = "menu"
    PAGINA = "pagina"
    FUNCIONALIDAD = "funcionalidad"
    API = "api"


class Modulo(Base):
    __tablename__ = "modulos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True, index=True)
    descripcion = Column(Text, nullable=True)
    ruta = Column(String(255), nullable=True)  # Ruta del módulo (ej: /usuarios, /dashboard)
    icono = Column(String(100), nullable=True)  # Icono para el frontend
    tipo = Column(SQLEnum(TipoModulo), default=TipoModulo.MENU, nullable=False)
    orden = Column(Integer, default=0, nullable=False)  # Orden de visualización
    is_active = Column(Boolean, default=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("modulos.id"), nullable=True)  # Para módulos anidados
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relación N a N con Usuarios
    usuarios = relationship(
        "UsuarioModulo",
        back_populates="modulo",
        cascade="all, delete-orphan"
    )
    
    # Relación N a N con Permisos
    permisos = relationship(
        "ModuloPermiso",
        back_populates="modulo",
        cascade="all, delete-orphan"
    )
    
    # Relación recursiva para módulos padre/hijo
    children = relationship("Modulo", backref="parent", remote_side=[id])

    def __repr__(self):
        return f"<Modulo(id={self.id}, nombre='{self.nombre}')>"
