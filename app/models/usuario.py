from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    nombre_completo = Column(String(200), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # Foreign Key a Rol (Relación N a 1)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Relaciones
    rol = relationship("Rol", back_populates="usuarios")
    
    # Relación N a N con Módulos
    modulos = relationship(
        "UsuarioModulo",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )
    
    # Relación 1 a 1 con Persona
    persona = relationship(
        "Persona",
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Usuario(id={self.id}, username='{self.username}')>"
