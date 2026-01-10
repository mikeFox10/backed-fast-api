from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Permiso(Base):
    __tablename__ = "permisos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True, index=True)
    codigo = Column(String(50), nullable=False, unique=True, index=True)  # Ej: "usuarios.crear", "usuarios.editar"
    descripcion = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relación N a N con Roles
    roles = relationship(
        "RolPermiso",
        back_populates="permiso",
        cascade="all, delete-orphan"
    )
    
    # Relación N a N con Módulos
    modulos = relationship(
        "ModuloPermiso",
        back_populates="permiso",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Permiso(id={self.id}, nombre='{self.nombre}', codigo='{self.codigo}')>"
