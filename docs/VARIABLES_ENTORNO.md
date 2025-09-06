# Variables de Entorno - Configuración Segura

## Variables Requeridas

### Configuración de Django
```bash
# Clave secreta para Django (OBLIGATORIA en producción)
SECRET_KEY=your-secret-key-here

# Modo debug (False en producción)
DEBUG=True

# Hosts permitidos (separados por comas)
ALLOWED_HOSTS=localhost,127.0.0.1,testserver
```

### Base de Datos
```bash
# URL de conexión a la base de datos
DATABASE_URL=sqlite:///db.sqlite3
# Para PostgreSQL: postgres://user:password@localhost:5432/dbname
```

### Redis (para Celery)
```bash
# URL de conexión a Redis
REDIS_URL=redis://localhost:6379/0
```

### CORS
```bash
# Permitir todos los orígenes (solo para desarrollo)
CORS_ALLOW_ALL_ORIGINS=True
```

### Render (para producción)
```bash
# Hostname externo de Render
RENDER_EXTERNAL_HOSTNAME=your-app.onrender.com
```

## Configuración para Desarrollo

Crea un archivo `.env` en la raíz del proyecto con:

```bash
SECRET_KEY=django-insecure-change-me-in-development
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,testserver
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
CORS_ALLOW_ALL_ORIGINS=True
```

## Configuración para Producción

En producción, configura estas variables en tu plataforma de despliegue:

```bash
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:password@host:port/dbname
REDIS_URL=redis://your-redis-host:6379/0
CORS_ALLOW_ALL_ORIGINS=False
RENDER_EXTERNAL_HOSTNAME=your-app.onrender.com
```

## Notas de Seguridad

1. **NUNCA** commites el archivo `.env` al control de versiones
2. **SIEMPRE** usa una SECRET_KEY única y segura en producción
3. **NUNCA** uses DEBUG=True en producción
4. Configura ALLOWED_HOSTS específicamente para tu dominio en producción
5. Usa HTTPS en producción y configura las variables de seguridad correspondientes
