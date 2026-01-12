"""
Seeders para poblar la base de datos con datos iniciales
"""
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.modulo import Modulo
from app.models.permiso import Permiso
from app.models.usuario_rol import UsuarioRol
from app.models.rol_modulo import RolModulo
from app.models.rol_permiso import RolPermiso
from app.models.modulo_permiso import ModuloPermiso
from app.models.modulo import TipoModulo
from app.models.persona import Persona, Genero
from datetime import date


def seed_permisos(db: Session):
    """Crear permisos iniciales"""
    permisos_data = [
        {"nombre": "Ver usuarios", "codigo": "usuarios.ver", "descripcion": "Permite ver la lista de usuarios"},
        {"nombre": "Crear usuarios", "codigo": "usuarios.crear", "descripcion": "Permite crear nuevos usuarios"},
        {"nombre": "Editar usuarios", "codigo": "usuarios.editar", "descripcion": "Permite editar usuarios existentes"},
        {"nombre": "Eliminar usuarios", "codigo": "usuarios.eliminar", "descripcion": "Permite eliminar usuarios"},
        {"nombre": "Ver roles", "codigo": "roles.ver", "descripcion": "Permite ver la lista de roles"},
        {"nombre": "Crear roles", "codigo": "roles.crear", "descripcion": "Permite crear nuevos roles"},
        {"nombre": "Editar roles", "codigo": "roles.editar", "descripcion": "Permite editar roles existentes"},
        {"nombre": "Eliminar roles", "codigo": "roles.eliminar", "descripcion": "Permite eliminar roles"},
        {"nombre": "Ver módulos", "codigo": "modulos.ver", "descripcion": "Permite ver la lista de módulos"},
        {"nombre": "Crear módulos", "codigo": "modulos.crear", "descripcion": "Permite crear nuevos módulos"},
        {"nombre": "Editar módulos", "codigo": "modulos.editar", "descripcion": "Permite editar módulos existentes"},
        {"nombre": "Eliminar módulos", "codigo": "modulos.eliminar", "descripcion": "Permite eliminar módulos"},
        {"nombre": "Ver permisos", "codigo": "permisos.ver", "descripcion": "Permite ver la lista de permisos"},
        {"nombre": "Crear permisos", "codigo": "permisos.crear", "descripcion": "Permite crear nuevos permisos"},
        {"nombre": "Editar permisos", "codigo": "permisos.editar", "descripcion": "Permite editar permisos existentes"},
        {"nombre": "Eliminar permisos", "codigo": "permisos.eliminar", "descripcion": "Permite eliminar permisos"},
    ]
    
    for permiso_data in permisos_data:
        existing = db.query(Permiso).filter(Permiso.codigo == permiso_data["codigo"]).first()
        if not existing:
            permiso = Permiso(**permiso_data)
            db.add(permiso)
    
    db.commit()
    print("✓ Permisos creados")


def seed_roles(db: Session):
    """Crear roles iniciales"""
    roles_data = [
        {
            "nombre": "Super Administrador",
            "descripcion": "Acceso completo al sistema",
            "permisos": [],  # Todos los permisos
            "modulos": []  # Todos los módulos
        },
        {
            "nombre": "Administrador",
            "descripcion": "Administrador con permisos limitados",
            "permisos": ["usuarios.ver", "usuarios.crear", "usuarios.editar", "roles.ver", "modulos.ver"],
            "modulos": ["Dashboard", "Usuarios", "Roles", "Módulos"]
        },
        {
            "nombre": "Usuario",
            "descripcion": "Usuario estándar",
            "permisos": ["usuarios.ver", "modulos.ver"],
            "modulos": ["Dashboard", "Usuarios"]
        },
    ]
    
    for rol_data in roles_data:
        existing = db.query(Rol).filter(Rol.nombre == rol_data["nombre"]).first()
        if not existing:
            modulos_nombres = rol_data.pop("modulos")
            rol = Rol(
                nombre=rol_data["nombre"],
                descripcion=rol_data["descripcion"]
            )
            db.add(rol)
            db.flush()
            
            # Asignar permisos
            if rol_data["nombre"] == "Super Administrador":
                # Todos los permisos
                permisos = db.query(Permiso).all()
            else:
                # Permisos específicos
                permisos = db.query(Permiso).filter(
                    Permiso.codigo.in_(rol_data["permisos"])
                ).all()
            
            for permiso in permisos:
                rol_permiso = RolPermiso(rol_id=rol.id, permiso_id=permiso.id)
                db.add(rol_permiso)
            
            # Asignar módulos
            if modulos_nombres:
                modulos = db.query(Modulo).filter(Modulo.nombre.in_(modulos_nombres)).all()
            else:
                # Todos los módulos
                modulos = db.query(Modulo).all()
            
            for modulo in modulos:
                rol_modulo = RolModulo(rol_id=rol.id, modulo_id=modulo.id, is_active=True)
                db.add(rol_modulo)
    
    db.commit()
    print("✓ Roles creados")


def seed_modulos(db: Session):
    """Crear módulos iniciales"""
    modulos_data = [
        {
            "nombre": "Dashboard",
            "descripcion": "Panel principal",
            "ruta": "/dashboard",
            "icono": "dashboard",
            "tipo": TipoModulo.MENU,
            "orden": 1,
            "permisos": []
        },
        {
            "nombre": "Usuarios",
            "descripcion": "Gestión de usuarios",
            "ruta": "/usuarios",
            "icono": "users",
            "tipo": TipoModulo.MENU,
            "orden": 2,
            "permisos": ["usuarios.ver", "usuarios.crear", "usuarios.editar", "usuarios.eliminar"]
        },
        {
            "nombre": "Roles",
            "descripcion": "Gestión de roles",
            "ruta": "/roles",
            "icono": "shield",
            "tipo": TipoModulo.MENU,
            "orden": 3,
            "permisos": ["roles.ver", "roles.crear", "roles.editar", "roles.eliminar"]
        },
        {
            "nombre": "Módulos",
            "descripcion": "Gestión de módulos",
            "ruta": "/modulos",
            "icono": "grid",
            "tipo": TipoModulo.MENU,
            "orden": 4,
            "permisos": ["modulos.ver", "modulos.crear", "modulos.editar", "modulos.eliminar"]
        },
        {
            "nombre": "Permisos",
            "descripcion": "Gestión de permisos",
            "ruta": "/permisos",
            "icono": "key",
            "tipo": TipoModulo.MENU,
            "orden": 5,
            "permisos": ["permisos.ver", "permisos.crear", "permisos.editar", "permisos.eliminar"]
        },
    ]
    
    for modulo_data in modulos_data:
        existing = db.query(Modulo).filter(Modulo.nombre == modulo_data["nombre"]).first()
        if not existing:
            permiso_ids = modulo_data.pop("permisos")
            modulo = Modulo(**modulo_data)
            db.add(modulo)
            db.flush()
            
            # Asignar permisos
            if permiso_ids:
                permisos = db.query(Permiso).filter(Permiso.codigo.in_(permiso_ids)).all()
                for permiso in permisos:
                    modulo_permiso = ModuloPermiso(modulo_id=modulo.id, permiso_id=permiso.id)
                    db.add(modulo_permiso)
    
    db.commit()
    print("✓ Módulos creados")


def seed_usuarios(db: Session):
    """Crear usuarios iniciales"""
    usuarios_data = [
        {
            "username": "admin",
            "email": "admin@example.com",
            "nombre_completo": "Administrador del Sistema",
            "password": "admin123",
            "is_superuser": True,
            "rol_nombre": "Super Administrador",
            "modulos": []  # Todos los módulos
        },
        {
            "username": "user1",
            "email": "user1@example.com",
            "nombre_completo": "Usuario de Prueba",
            "password": "user123",
            "is_superuser": False,
            "rol_nombre": "Usuario",
            "modulos": ["Dashboard", "Usuarios"]
        },
    ]
    
    for usuario_data in usuarios_data:
        existing = db.query(Usuario).filter(Usuario.username == usuario_data["username"]).first()
        if not existing:
            rol_nombre = usuario_data.pop("rol_nombre")
            password = usuario_data.pop("password")
            usuario_data.pop("modulos")  # Ya no se asignan directamente
            
            rol = db.query(Rol).filter(Rol.nombre == rol_nombre).first()
            
            usuario = Usuario(
                username=usuario_data["username"],
                email=usuario_data["email"],
                nombre_completo=usuario_data["nombre_completo"],
                hashed_password=get_password_hash(password),
                is_superuser=usuario_data["is_superuser"]
            )
            db.add(usuario)
            db.flush()
            
            # Asignar rol al usuario
            if rol:
                usuario_rol = UsuarioRol(usuario_id=usuario.id, rol_id=rol.id, is_active=True)
                db.add(usuario_rol)
    
    db.commit()
    print("✓ Usuarios creados")
    print("\n  Credenciales de acceso:")
    print("  - Usuario: admin / Contraseña: admin123")
    print("  - Usuario: user1 / Contraseña: user123")


def seed_personas(db: Session):
    """Crear personas para usuarios iniciales"""
    from app.models.usuario import Usuario
    
    # Persona para admin
    admin = db.query(Usuario).filter(Usuario.username == "admin").first()
    if admin:
        existing = db.query(Persona).filter(Persona.usuario_id == admin.id).first()
        if not existing:
            persona_admin = Persona(
                usuario_id=admin.id,
                dni="12345678",
                fecha_nacimiento=date(1990, 1, 15),
                genero=Genero.MASCULINO,
                telefono="+1234567890",
                direccion="Calle Principal 123",
                ciudad="Ciudad Capital",
                estado_provincia="Estado",
                codigo_postal="12345",
                pais="España",
                biografia="Administrador principal del sistema",
                linkedin="https://linkedin.com/in/admin",
                github="https://github.com/admin"
            )
            db.add(persona_admin)
    
    # Persona para user1
    user1 = db.query(Usuario).filter(Usuario.username == "user1").first()
    if user1:
        existing = db.query(Persona).filter(Persona.usuario_id == user1.id).first()
        if not existing:
            persona_user1 = Persona(
                usuario_id=user1.id,
                dni="87654321",
                fecha_nacimiento=date(1995, 6, 20),
                genero=Genero.FEMENINO,
                telefono="+0987654321",
                telefono_alternativo="+1111111111",
                email_alternativo="user1.alternativo@example.com",
                direccion="Avenida Secundaria 456",
                ciudad="Ciudad Secundaria",
                estado_provincia="Provincia",
                codigo_postal="54321",
                pais="España",
                biografia="Usuario de prueba del sistema",
                sitio_web="https://user1.example.com",
                twitter="https://twitter.com/user1"
            )
            db.add(persona_user1)
    
    db.commit()
    print("✓ Personas creadas")


def run_seeders():
    """Ejecutar todos los seeders"""
    db = SessionLocal()
    try:
        print("Iniciando seeders...\n")
        seed_permisos(db)
        seed_roles(db)
        seed_modulos(db)
        seed_usuarios(db)
        seed_personas(db)
        print("\n✓ Seeders completados exitosamente")
    except Exception as e:
        print(f"\n✗ Error en seeders: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seeders()
