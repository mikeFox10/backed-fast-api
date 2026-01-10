from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class ModuloPermiso(Base):
    """
    Tabla intermedia para relación N a N entre Módulos y Permisos
    """
    __tablename__ = "modulo_permiso"

    id = Column(Integer, primary_key=True, index=True)
    modulo_id = Column(Integer, ForeignKey("modulos.id"), nullable=False)
    permiso_id = Column(Integer, ForeignKey("permisos.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    fecha_asignacion = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    modulo = relationship("Modulo", back_populates="permisos")
    permiso = relationship("Permiso", back_populates="modulos")

    def __repr__(self):
        return f"<ModuloPermiso(modulo_id={self.modulo_id}, permiso_id={self.permiso_id})>"
