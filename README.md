# Backend Gestión de Usuarios y Permisos - FastAPI

Backend FastAPI que implementa un sistema completo de gestión de usuarios, roles, módulos y permisos

## 🚀 Características

- ✅ **Autenticación JWT** - Sistema de autenticación seguro con tokens
- ✅ **Gestión de Usuarios** - CRUD completo de usuarios
- ✅ **Sistema de Roles** - Asignación de roles a usuarios (1 a N)
- ✅ **Módulos** - Gestión de módulos del sistema (1 a N con usuarios)
- ✅ **Permisos** - Sistema granular de permisos (N a N con roles y módulos)
- ✅ **Variables de Entorno** - Configuración mediante `.env`
- ✅ **Migraciones con Alembic** - Control de versiones de base de datos
- ✅ **Seeders** - Datos iniciales para desarrollo
- ✅ **Middlewares** - Logging, CORS, manejo de errores
- ✅ **Docker Compose** - Despliegue fácil con PostgreSQL
- ✅ **Documentación Automática** - Swagger/OpenAPI en `/docs`

## 📋 Requisitos Previos

- Docker y Docker Compose
- Python 3.11+ (modo local)

## 🛠️ Instalación y Uso

### Con Docker Compose

1. **Clonar el repositorio**

2. **Crear y configurar variables de entorno**:
   ```bash
   cp .env.example .env
   ```

3. **Construir y ejecutar**:
   ```bash
   docker-compose up --build
   ```

4. **Acceder a la aplicación**:
   - API: http://localhost:8000
   - Documentación: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Sin Docker (Desarrollo Local)

1. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar base de datos PostgreSQL**:
   - Crear una base de datos PostgreSQL
   - Actualiza `DATABASE_URL` en `.env`

4. **Ejecutar migraciones**:
   ```bash
   alembic upgrade head
   ```

5. **Ejecutar seeders**:
   ```bash
   python -m app.db.seeders
   ```

6. **Iniciar servidor**:
   ```bash
   uvicorn app.main:app --reload
   ```

## 📊 Estructura del Proyecto

```
crud-fastapi/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py          # Endpoints de autenticación
│   │       ├── usuarios.py      # CRUD de usuarios
│   │       ├── roles.py          # CRUD de roles
│   │       ├── modulos.py        # CRUD de módulos
│   │       └── permisos.py       # CRUD de permisos
│   ├── core/
│   │   ├── config.py             # Configuración y variables de entorno
│   │   ├── database.py           # Configuración de SQLAlchemy
│   │   ├── security.py           # JWT y seguridad
│   │   └── middleware.py         # Middlewares personalizados
│   ├── models/                   # Modelos SQLAlchemy
│   │   ├── usuario.py
│   │   ├── rol.py
│   │   ├── modulo.py
│   │   ├── permiso.py
│   │   └── relaciones (N a N)
│   ├── schemas/                  # Schemas Pydantic
│   ├── services/                 # Lógica de negocio
│   └── db/
│       └── seeders.py            # Datos iniciales
├── alembic/                      # Migraciones
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🔐 Usuarios por Defecto

- **Super Administrador**:
  - Usuario: `admin`
  - Contraseña: `admin123`

- **Usuario Estándar**:
  - Usuario: `user1`
  - Contraseña: `user123`

## 📡 Endpoints Principales

### Autenticación
- `POST /api/v1/auth/login` - Login (form data)
- `POST /api/v1/auth/login/json` - Login (JSON)
- `GET /api/v1/auth/me` - Usuario actual

### Usuarios
- `GET /api/v1/usuarios` - Listar usuarios
- `GET /api/v1/usuarios/{id}` - Obtener usuario
- `POST /api/v1/usuarios` - Crear usuario
- `PUT /api/v1/usuarios/{id}` - Actualizar usuario
- `DELETE /api/v1/usuarios/{id}` - Eliminar usuario
- `POST /api/v1/usuarios/{id}/roles` - Asignar roles (los módulos se calculan automáticamente)

### Roles
- `GET /api/v1/roles` - Listar roles
- `GET /api/v1/roles/{id}` - Obtener rol
- `POST /api/v1/roles` - Crear rol
- `PUT /api/v1/roles/{id}` - Actualizar rol
- `DELETE /api/v1/roles/{id}` - Eliminar rol
- `POST /api/v1/roles/{id}/permisos` - Asignar permisos
- `POST /api/v1/roles/{id}/modulos` - Asignar módulos

### Módulos
- `GET /api/v1/modulos` - Listar módulos
- `GET /api/v1/modulos/{id}` - Obtener módulo
- `POST /api/v1/modulos` - Crear módulo
- `PUT /api/v1/modulos/{id}` - Actualizar módulo
- `DELETE /api/v1/modulos/{id}` - Eliminar módulo
- `POST /api/v1/modulos/{id}/permisos` - Asignar permisos

### Permisos
- `GET /api/v1/permisos` - Listar permisos
- `GET /api/v1/permisos/{id}` - Obtener permiso
- `POST /api/v1/permisos` - Crear permiso
- `PUT /api/v1/permisos/{id}` - Actualizar permiso
- `DELETE /api/v1/permisos/{id}` - Eliminar permiso

## 🔗 Relaciones

- **Usuario → Roles**: N a N (Un usuario puede tener múltiples roles)
- **Rol → Módulos**: N a N (Un rol puede tener acceso a múltiples módulos)
- **Rol → Permisos**: N a N (Un rol puede tener múltiples permisos)
- **Módulo → Permisos**: N a N (Un módulo puede requerir múltiples permisos)

### Diseño de Accesos

Los módulos a los que un usuario tiene acceso se **calculan dinámicamente** desde los roles asignados:
- Si un usuario tiene múltiples roles, tiene acceso a todos los módulos de todos sus roles
- Si un módulo está en varios roles del usuario, se incluye una sola vez (sin duplicados)
- Los permisos se activan si **al menos uno** de los roles del usuario tiene acceso al módulo

## 🧪 Migraciones

### Crear nueva migración:
```bash
alembic revision --autogenerate -m "descripción"
```

### Aplicar migraciones:
```bash
alembic upgrade head
```

### Revertir migración:
```bash
alembic downgrade -1
```


## 📝 Variables de Entorno

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=crud_fastapi
DATABASE_URL=postgresql://postgres:postgres@db:5432/crud_fastapi

# Security
SECRET_KEY=tu-clave-secreta-super-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development
DEBUG=True
```

## 🐳 Comandos 

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f api

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Reconstruir
docker-compose up --build
```

## 📚 Documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc


## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
