# Configuración Centralizada SIPI

Este archivo documenta la configuración centralizada del proyecto SIPI.

## Ubicación de Variables de Entorno

**Archivo principal**: `C:\Users\admin\dev\sipi-core\.env`

Este archivo `.env` es la **fuente única de verdad** para toda la configuración del proyecto y es compartido entre:
- Backend (sipi-api)
- Frontend (sipi-frontend)
- Scripts y herramientas (sipi-core)

## Variables Configuradas

### Base de Datos (Supabase)
```env
DATABASE_URL=postgresql+asyncpg://postgres.edgrrunsbyhutbceafuf:jO04ufJ7R06LWRLE@aws-1-eu-west-1.pooler.supabase.com:5432/postgres
DATABASE_SCHEMA=sipi
```

### API GraphQL Backend
```env
API_HOST=localhost
API_PORT=8040
API_URL=http://localhost:8040/graphql
```

### Frontend (Vite)
```env
VITE_API_URL=http://localhost:8040/graphql
VITE_GRAPHQL_URL=http://localhost:8040/graphql
```

## Cómo Usar

### Backend (sipi-api)
El backend carga automáticamente el `.env` desde el directorio donde se ejecuta o desde las variables de entorno del sistema.

### Frontend (sipi-frontend)
El frontend está configurado en `vite.config.js` para cargar el `.env` desde `sipi-core`:

```javascript
const env = loadEnv(mode, path.resolve(__dirname, '../sipi-core'), '')
```

Las variables `VITE_*` son expuestas automáticamente al código del frontend y pueden ser accedidas con:

```javascript
import.meta.env.VITE_API_URL
import.meta.env.VITE_GRAPHQL_URL
```

## Servicios Activos

### Backend GraphQL API
- **URL**: http://localhost:8040/graphql
- **GraphiQL**: http://localhost:8040/graphql
- **OpenAPI Docs**: http://localhost:8040/docs
- **Health Check**: http://localhost:8040/health

### Frontend
- **URL**: http://localhost:5177/ (o el puerto disponible que Vite encuentre)

## Cambiar Configuración

Para cambiar la configuración del proyecto:

1. Editar **únicamente** el archivo `C:\Users\admin\dev\sipi-core\.env`
2. Reiniciar los servicios que necesites actualizar:
   - Backend: Reiniciar uvicorn
   - Frontend: Reiniciar vite (se recarga automáticamente en modo dev)

## Notas Importantes

- ✅ **NO** crear archivos `.env` en otros directorios (sipi-api, sipi-frontend)
- ✅ **NO** hardcodear URLs o puertos en el código
- ✅ **SIEMPRE** usar variables de entorno para configuración
- ✅ El archivo `.env` **NO** debe committearse a git (está en .gitignore)
