from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException, status
from app.models.persona import Persona
from app.models.usuario import Usuario
from app.schemas.persona import PersonaCreate, PersonaUpdate


class PersonaService:
    @staticmethod
    def get_persona(db: Session, usuario_id: int) -> Optional[Persona]:
        """Obtener persona por usuario_id"""
        return db.query(Persona).filter(Persona.usuario_id == usuario_id).first()

    @staticmethod
    def get_persona_by_dni(db: Session, dni: str) -> Optional[Persona]:
        """Obtener persona por DNI"""
        return db.query(Persona).filter(Persona.dni == dni).first()

    @staticmethod
    def create_persona(
        db: Session,
        usuario_id: int,
        datos: PersonaCreate
    ) -> Persona:
        """Crear persona para un usuario"""
        # Verificar que el usuario existe
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar que el usuario no tenga ya una persona
        existing = PersonaService.get_persona(db, usuario_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya tiene datos personales. Use actualizar en su lugar."
            )
        
        # Verificar DNI único si se proporciona
        if datos.dni:
            if PersonaService.get_persona_by_dni(db, datos.dni):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El DNI ya está en uso"
                )
        
        db_persona = Persona(usuario_id=usuario_id, **datos.model_dump(exclude_unset=True))
        db.add(db_persona)
        db.commit()
        db.refresh(db_persona)
        return db_persona

    @staticmethod
    def update_persona(
        db: Session,
        usuario_id: int,
        datos_update: PersonaUpdate
    ) -> Persona:
        """Actualizar persona de un usuario"""
        db_persona = PersonaService.get_persona(db, usuario_id)
        
        if not db_persona:
            # Si no existe, crearla
            datos_create = PersonaCreate(**datos_update.model_dump(exclude_unset=True))
            return PersonaService.create_persona(db, usuario_id, datos_create)
        
        # Verificar DNI único si se está actualizando
        if datos_update.dni and datos_update.dni != db_persona.dni:
            if PersonaService.get_persona_by_dni(db, datos_update.dni):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El DNI ya está en uso"
                )
            db_persona.dni = datos_update.dni
        
        # Actualizar otros campos
        update_data = datos_update.model_dump(exclude_unset=True, exclude={"dni"})
        for field, value in update_data.items():
            setattr(db_persona, field, value)
        
        db.commit()
        db.refresh(db_persona)
        return db_persona

    @staticmethod
    def delete_persona(db: Session, usuario_id: int) -> bool:
        """Eliminar persona de un usuario"""
        db_persona = PersonaService.get_persona(db, usuario_id)
        if not db_persona:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Persona no encontrada"
            )
        
        db.delete(db_persona)
        db.commit()
        return True
