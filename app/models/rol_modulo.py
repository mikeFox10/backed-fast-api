from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class RolModulo(Base):
    """
    Tabla intermedia para relación N a N entre Roles y Módulos
    """
    __tablename__ = "rol_modulo"

    id = Column(Integer, primary_key=True, index=True)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    modulo_id = Column(Integer, ForeignKey("modulos.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    fecha_asignacion = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    rol = relationship("Rol", back_populates="modulos")
    modulo = relationship("Modulo", back_populates="roles")

    def __repr__(self):
        return f"<RolModulo(rol_id={self.rol_id}, modulo_id={self.modulo_id})>"
