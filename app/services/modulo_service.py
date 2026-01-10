from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from app.models.modulo import Modulo
from app.models.modulo_permiso import ModuloPermiso
from app.schemas.modulo import ModuloCreate, ModuloUpdate


class ModuloService:
    @staticmethod
    def get_modulo(db: Session, modulo_id: int) -> Optional[Modulo]:
        """Obtener módulo por ID"""
        return db.query(Modulo).filter(Modulo.id == modulo_id).first()

    @staticmethod
    def get_modulo_by_nombre(db: Session, nombre: str) -> Optional[Modulo]:
        """Obtener módulo por nombre"""
        return db.query(Modulo).filter(Modulo.nombre == nombre).first()

    @staticmethod
    def get_modulos(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        parent_id: Optional[int] = None
    ) -> List[Modulo]:
        """Obtener lista de módulos"""
        query = db.query(Modulo)
        if is_active is not None:
            query = query.filter(Modulo.is_active == is_active)
        if parent_id is not None:
            query = query.filter(Modulo.parent_id == parent_id)
        return query.order_by(Modulo.orden).offset(skip).limit(limit).all()

    @staticmethod
    def create_modulo(db: Session, modulo: ModuloCreate) -> Modulo:
        """Crear nuevo módulo"""
        if ModuloService.get_modulo_by_nombre(db, modulo.nombre):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre del módulo ya existe"
            )
        
        db_modulo = Modulo(
            nombre=modulo.nombre,
            descripcion=modulo.descripcion,
            ruta=modulo.ruta,
            icono=modulo.icono,
            tipo=modulo.tipo,
            orden=modulo.orden,
            is_active=modulo.is_active,
            parent_id=modulo.parent_id
        )
        db.add(db_modulo)
        db.commit()
        db.refresh(db_modulo)
        
        # Asignar permisos
        if modulo.permiso_ids:
            ModuloService.asignar_permisos(db, db_modulo.id, modulo.permiso_ids)
            db.refresh(db_modulo)
        
        return db_modulo

    @staticmethod
    def update_modulo(db: Session, modulo_id: int, modulo_update: ModuloUpdate) -> Modulo:
        """Actualizar módulo"""
        db_modulo = ModuloService.get_modulo(db, modulo_id)
        if not db_modulo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Módulo no encontrado"
            )
        
        if modulo_update.nombre and modulo_update.nombre != db_modulo.nombre:
            if ModuloService.get_modulo_by_nombre(db, modulo_update.nombre):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre del módulo ya existe"
                )
            db_modulo.nombre = modulo_update.nombre
        
        if modulo_update.descripcion is not None:
            db_modulo.descripcion = modulo_update.descripcion
        if modulo_update.ruta is not None:
            db_modulo.ruta = modulo_update.ruta
        if modulo_update.icono is not None:
            db_modulo.icono = modulo_update.icono
        if modulo_update.tipo is not None:
            db_modulo.tipo = modulo_update.tipo
        if modulo_update.orden is not None:
            db_modulo.orden = modulo_update.orden
        if modulo_update.is_active is not None:
            db_modulo.is_active = modulo_update.is_active
        if modulo_update.parent_id is not None:
            db_modulo.parent_id = modulo_update.parent_id
        
        if modulo_update.permiso_ids is not None:
            ModuloService.asignar_permisos(db, modulo_id, modulo_update.permiso_ids)
        
        db.commit()
        db.refresh(db_modulo)
        return db_modulo

    @staticmethod
    def delete_modulo(db: Session, modulo_id: int) -> bool:
        """Eliminar módulo"""
        db_modulo = ModuloService.get_modulo(db, modulo_id)
        if not db_modulo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Módulo no encontrado"
            )
        
        db.delete(db_modulo)
        db.commit()
        return True

    @staticmethod
    def asignar_permisos(db: Session, modulo_id: int, permiso_ids: List[int]) -> Modulo:
        """Asignar permisos a módulo"""
        db_modulo = ModuloService.get_modulo(db, modulo_id)
        if not db_modulo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Módulo no encontrado"
            )
        
        # Eliminar asignaciones existentes
        db.query(ModuloPermiso).filter(ModuloPermiso.modulo_id == modulo_id).delete()
        
        # Crear nuevas asignaciones
        for permiso_id in permiso_ids:
            modulo_permiso = ModuloPermiso(
                modulo_id=modulo_id,
                permiso_id=permiso_id,
                is_active=True
            )
            db.add(modulo_permiso)
        
        db.commit()
        db.refresh(db_modulo)
        return db_modulo
