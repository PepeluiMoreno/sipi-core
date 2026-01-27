# Configuracion Centralizada SIPI

## Archivos de Configuracion

| Archivo | Proposito |
|---------|-----------|
| `sipi-core/.env` | Selector de entorno (development/production) |
| `sipi-core/.env.development` | Variables para desarrollo local |
| `sipi-core/.env.production` | Variables para produccion |
| `sipi-core/config.py` | Modulo Python que carga la configuracion |

## Cambiar de Entorno

Editar `sipi-core/.env`:

```env
# Para desarrollo
ENVIRONMENT=development

# Para produccion
ENVIRONMENT=production
```

El sistema cargara automaticamente `.env.development` o `.env.production`.

## Variables de Entorno

### Development (.env.development)

```env
ENVIRONMENT=development
DATABASE_URL=postgresql+asyncpg://sipi:sipi@localhost:5432/sipi
DATABASE_SCHEMA=sipi
API_HOST=0.0.0.0
API_PORT=8040
API_URL=http://localhost:8040/graphql
VITE_API_URL=http://localhost:8040/graphql
```

### Production (.env.production)

```env
ENVIRONMENT=production
FRONTEND_DOMAIN=sipi.europalaica.org
API_DOMAIN=sipi-api.europalaica.org
DATABASE_URL=postgresql+asyncpg://user:pass@sipi-db:5432/sipi
API_URL=https://sipi-api.europalaica.org/graphql
VITE_API_URL=https://sipi-api.europalaica.org/graphql
```

## Uso en Python

```python
from config import CONFIG

print(CONFIG.DATABASE_URL)
print(CONFIG.API_PORT)
print(CONFIG.ENVIRONMENT)  # development o production
print(CONFIG.DEBUG)        # True en development
```

## Uso en Frontend (Vite)

```javascript
// vite.config.js carga desde sipi-core
const env = loadEnv(mode, path.resolve(__dirname, '../sipi-core'), '')

// En codigo
import.meta.env.VITE_API_URL
```

## Servicios (Development)

| Servicio | URL |
|----------|-----|
| GraphQL API | http://localhost:8040/graphql |
| Health Check | http://localhost:8040/health |
| Frontend | http://localhost:5173 |

## Servicios (Production)

| Servicio | URL |
|----------|-----|
| Frontend | https://sipi.europalaica.org |
| GraphQL API | https://sipi-api.europalaica.org/graphql |

## Reglas

- Editar `.env` solo para cambiar el entorno
- Editar `.env.development` o `.env.production` para cambiar valores
- No crear .env en sipi-api ni sipi-frontend
- No hardcodear valores en el codigo
- Los archivos .env no se commitean (estan en .gitignore)
