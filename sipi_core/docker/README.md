# Docker - Despliegue de Produccion

## Estructura

```
docker/
├── Dockerfile.api          # Imagen del backend
├── Dockerfile.frontend     # Imagen del frontend
├── docker-compose.yml      # Orquestacion de servicios
├── init-db.sql            # Script de inicializacion de BD
├── .dockerignore
└── nginx/
    ├── nginx.conf         # Configuracion principal nginx
    ├── frontend.conf      # Config para contenedor frontend
    └── conf.d/
        └── default.conf   # Reverse proxy config
```

## Subdominios

| Subdominio | Servicio |
|------------|----------|
| sipi.europalaica.org | Frontend Vue |
| sipi-api.europalaica.org | API GraphQL |

## Configuracion

1. Copiar `.env.production` a `.env` y ajustar valores:

```bash
cp ../.env.production .env
```

2. Editar `.env` con valores reales:

```env
DB_PASSWORD=contraseña_segura
SSL_CERT_PATH=/etc/letsencrypt/live/europalaica.org/fullchain.pem
SSL_KEY_PATH=/etc/letsencrypt/live/europalaica.org/privkey.pem
```

## DNS

Configurar registros DNS tipo A o CNAME apuntando al servidor:

```
sipi.europalaica.org      → IP_SERVIDOR
sipi-api.europalaica.org  → IP_SERVIDOR
```

## Despliegue

```bash
# Construir imagenes
docker-compose build

# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

## Servicios

| Servicio | Puerto | Descripcion |
|----------|--------|-------------|
| nginx | 80, 443 | Reverse proxy |
| api | 8040 | Backend GraphQL |
| frontend | 3000 | Frontend Vue |
| db | 5432 | PostgreSQL/PostGIS |

## SSL

Obtener certificado wildcard con Let's Encrypt:

```bash
certbot certonly --manual --preferred-challenges dns -d "*.europalaica.org" -d "europalaica.org"
```

O certificados individuales:

```bash
certbot certonly --standalone -d sipi.europalaica.org -d sipi-api.europalaica.org
```
