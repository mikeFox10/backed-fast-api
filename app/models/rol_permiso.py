from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class RolPermiso(Base):
    """
    Tabla intermedia para relación N a N entre Roles y Permisos
    """
    __tablename__ = "rol_permiso"

    id = Column(Integer, primary_key=True, index=True)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    permiso_id = Column(Integer, ForeignKey("permisos.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    fecha_asignacion = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    rol = relationship("Rol", back_populates="permisos")
    permiso = relationship("Permiso", back_populates="roles")

    def __repr__(self):
        return f"<RolPermiso(rol_id={self.rol_id}, permiso_id={self.permiso_id})>"
