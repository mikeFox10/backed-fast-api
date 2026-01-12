from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class Genero(str, enum.Enum):
    MASCULINO = "masculino"
    FEMENINO = "femenino"
    OTRO = "otro"
    PREFIERO_NO_DECIR = "prefiero_no_decir"


class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Key a Usuario (Relación 1 a 1)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, unique=True, index=True)
    
    # Datos de identificación
    dni = Column(String(20), nullable=True, unique=True, index=True)
    fecha_nacimiento = Column(Date, nullable=True)
    genero = Column(SQLEnum(Genero), nullable=True)
    
    # Datos de contacto
    telefono = Column(String(20), nullable=True)
    telefono_alternativo = Column(String(20), nullable=True)
    email_alternativo = Column(String(255), nullable=True)
    
    # Dirección
    direccion = Column(Text, nullable=True)
    ciudad = Column(String(100), nullable=True)
    estado_provincia = Column(String(100), nullable=True)
    codigo_postal = Column(String(20), nullable=True)
    pais = Column(String(100), nullable=True)
    
    # Información adicional
    foto_perfil = Column(String(500), nullable=True)  # URL o path de la imagen
    biografia = Column(Text, nullable=True)
    sitio_web = Column(String(255), nullable=True)
    
    # Redes sociales (opcional, podrían ser campos JSON en el futuro)
    linkedin = Column(String(255), nullable=True)
    twitter = Column(String(255), nullable=True)
    github = Column(String(255), nullable=True)
    
    # Metadatos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relación 1 a 1 con Usuario
    usuario = relationship("Usuario", back_populates="persona", uselist=False)

    def __repr__(self):
        return f"<Persona(id={self.id}, usuario_id={self.usuario_id})>"
