from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class UsuarioModulo(Base):
    """
    Tabla intermedia para relación N a N entre Usuarios y Módulos
    """
    __tablename__ = "usuario_modulo"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    modulo_id = Column(Integer, ForeignKey("modulos.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    fecha_asignacion = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="modulos")
    modulo = relationship("Modulo", back_populates="usuarios")

    def __repr__(self):
        return f"<UsuarioModulo(usuario_id={self.usuario_id}, modulo_id={self.modulo_id})>"
