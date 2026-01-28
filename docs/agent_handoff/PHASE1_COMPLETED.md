# Phase 1: Core Architecture - COMPLETED ✅

**Fecha de completado**: 2025-12-21
**Estado**: ✅ MIGRACIÓN APLICADA - Base de datos operativa en Supabase

---

## 📋 Resumen Ejecutivo

La Fase 1 del sistema de inteligencia SIPI está **completada y desplegada**. Se han creado todos los modelos de datos necesarios, configurado GraphQL para auto-generación de API, y aplicado exitosamente la migración de base de datos en Supabase.

**Estado actual**:
- ✅ 51 tablas creadas en schema `sipi`
- ✅ PostGIS habilitado para datos geográficos
- ✅ Todos los modelos Phase 1 (`OSMPlace`, `InmuebleLifecycle`) creados
- ✅ 5 nuevos campos añadidos a `Inmueble`
- ✅ Migración Alembic aplicada (revision: `240ba0d4cbd7`)

---

## 🎯 Objetivos Completados

### 1. Modelos de Datos en `sipi-core`

#### ✅ OSMPlace (`sipi/db/models/osm.py`)
Censo local de lugares extraídos de OpenStreetMap para geolocalización.

**Campos**:
- `osm_id` (String, unique, indexed) - ID original de OSM
- `name` (String, indexed) - Nombre del lugar
- `amenity` (String, indexed) - Tipo de amenidad
- `religion`, `denomination` - Clasificación religiosa
- `municipio_id` (String, indexed) - Vínculo con municipio
- `addr_city`, `addr_postcode` - Dirección normalizada
- `geom` (Geometry POINT) - Coordenadas geográficas
- `tags` (JSONB) - Tags adicionales de OSM

**Ubicación**: `sipi-core/sipi/db/models/osm.py`

---

#### ✅ EventoHistorial (`sipi/db/models/historial.py`)
Expediente/Bitácora del inmueble: eventos detectados automáticamente.

**Campos**:
- `inmueble_id` (FK a Inmueble, indexed)
- `event_type` (ENUM, indexed) - Tipo de evento
- `event_date` (TIMESTAMP, indexed) - Fecha del evento
- `details` (JSONB) - Detalles específicos del evento
- `description` (Text) - Descripción legible
- `source` (String) - Origen del evento (Manual, Scraper-BOE, etc.)

**Tipos de Eventos** (`TipoEventoHistorial`):
- `ALTA_INMATRICULACION` - Registro inicial
- `PUESTA_EN_VENTA` - Inmueble sale al mercado
- `VENDIDO` - Inmueble vendido
- `CAMBIO_DE_USO` - Cambio de uso del inmueble
- `REHABILITACION` - Obra de rehabilitación
- `REHABILITACION_SUBVENCIONADA` - Rehabilitación con subvención pública
- `DECLARACION_BIC` - Declarado Bien de Interés Cultural
- `CAMBIO_VISITABILIDAD` - Cambio en régimen de visitas

**Ubicación**: `sipi-core/sipi/db/models/historial.py`

---

#### ✅ Inmueble - Campos Añadidos (`sipi/db/models/inmuebles.py`)

**Nuevos campos**:

1. **`estado_ciclo_vida`** (ENUM, indexed, default: INMATRICULADO)
   - `INMATRICULADO` - Registrado en propiedad
   - `EN_VENTA` - Puesto a la venta
   - `VENDIDO` - Vendido
   - `CAMBIO_DE_USO` - Cambió de uso

2. **`geo_quality`** (ENUM, indexed, default: MISSING)
   - `MANUAL` - Validado por humano
   - `AUTO` - Asignado por script
   - `MISSING` - Sin coordenadas

3. **`es_visitable`** (Boolean, default: False)
   - Indica si el inmueble permite visitas públicas

4. **`horario_visitas`** (Text, nullable)
   - Horario de visitas (formato libre o JSON)
   - **Nota**: No hay validación en backend. El frontend mostrará este campo como obligatorio si el inmueble es BIC + Visitable.

5. **`enlace_web_visitas`** (String 500, nullable)
   - URL con información de visitas

**Ubicación**: `sipi-core/sipi/db/models/inmuebles.py:28-95`

---

### 2. GraphQL API Auto-Generada

#### ✅ Configuración de Schema (`sipi-api/app/graphql/schema.py`)

**Cambios implementados**:

1. **`load_all_models()`** - Actualizada para importar desde `sipi.db.models`
   - Líneas 49-70: Ahora detecta si el parámetro es un paquete Python
   - Importa directamente desde `sipi-core` en lugar de buscar archivos locales

2. **`create_schema()`** - Parámetro por defecto cambiado a `"sipi.db.models"`
   - Línea 569: `models_folder: str = "sipi.db.models"`

**Resultado**:
- GraphQL auto-genera tipos para `OSMPlace`, `EventoHistorial`, `Inmueble`
- Queries disponibles: `getOSMPlace`, `osmPlaces`, `getEventoHistorial`, `eventosExpediente`, etc.
- Mutations disponibles: `createOSMPlace`, `createEventoHistorial`, `updateInmueble`, etc.

**Ubicación**: `sipi-api/app/graphql/schema.py`

---

### 3. Migración de Base de Datos

#### ✅ Alembic Configurado para Async (`sipi-api/alembic/env.py`)

**Cambios**:
- Líneas 1-71: Soporte completo para driver `asyncpg`
- Línea 10: `load_dotenv()` - Carga variables desde `.env`
- Líneas 56-66: Función async `run_migrations_online()`

**Ubicación**: `sipi-api/alembic/env.py`

---

#### ✅ Migración Creada y Aplicada (`alembic/versions/240ba0d4cbd7_*.py`)

**Revision ID**: `240ba0d4cbd7`
**Parent**: None (Migración inicial consolidada)

**Nota**: Esta es ahora la migración inicial única que crea toda la estructura de la base de datos desde cero, incluyendo los modelos originales y los de Phase 1.

**Operaciones**:

1. **Crear ENUM types** (líneas 22-27):
   - `estadociclovida` (4 valores)
   - `geoquality` (3 valores)
   - `lifecycleeventtype` (8 valores)

2. **Crear tabla `osm_places`** (líneas 30-46):
   - Schema: `sipi`
   - 14 columnas + audit fields
   - Índices en: `osm_id` (unique), `name`, `amenity`, `municipio_id`
   - Geometría: Point SRID 4326

3. **Crear tabla `inmueble_lifecycle`** (líneas 49-61):
   - Schema: `sipi`
   - FK a `sipi.inmuebles`
   - Índices en: `inmueble_id`, `event_type`, `event_date`

4. **Añadir 5 columnas a `inmuebles`** (líneas 64-68):
   - `estado_ciclo_vida` (ENUM, default: 'inmatriculado')
   - `geo_quality` (ENUM, default: 'missing')
   - `es_visitable` (Boolean, default: false)
   - `horario_visitas` (Text, nullable)
   - `enlace_web_visitas` (String 500, nullable)

**Rollback**: Función `downgrade()` revierte todos los cambios (líneas 71-86)

**Ubicación**: `sipi-api/alembic/versions/240ba0d4cbd7_add_osmplace_inmueblelifecycle_and_.py`

---

### 4. Configuración de Infraestructura

#### ✅ Variables de Entorno Supabase (`sipi-api/.env`)

**Configuración actualizada**:
```env
POSTGRES_USER=postgres.edgrrunsbyhutbceafuf
POSTGRES_PASSWORD=jO04ufJ7R06LWRLE
POSTGRES_DB=postgres
POSTGRES_SERVICE_NAME=aws-1-eu-west-1.pooler.supabase.com
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://postgres.edgrrunsbyhutbceafuf:jO04ufJ7R06LWRLE@aws-1-eu-west-1.pooler.supabase.com:5432/postgres
DATABASE_SCHEMA=sipi
```

**Extensiones habilitadas en Supabase**:
- `postgis` (3.3.7) - Para tipos geometry/geography
- `pgcrypto` (1.3) - Para gen_random_uuid()

**Ubicación**: `sipi-api/.env`

---

## 🚀 Próximos Pasos

### ✅ Completado

1. **Migración aplicada exitosamente**:
   - Estado: `240ba0d4cbd7 (head)`
   - 51 tablas creadas en schema `sipi`
   - Todos los modelos de Phase 1 disponibles

2. **Verificación realizada**:
   - ✅ `osm_places` creada
   - ✅ `inmueble_lifecycle` creada
   - ✅ 5 nuevos campos en `inmuebles`
   - ✅ 3 nuevos ENUMs (estadociclovida, geoquality, lifecycleeventtype)

### Siguiente: Probar GraphQL API

1. **Iniciar API**:
   ```bash
   cd sipi-api
   uvicorn app.graphql.app:application --reload
   ```

2. **Abrir GraphiQL**: `http://localhost:8040/graphql`

3. **Query de prueba**:
   ```graphql
   query {
     inmuebles(limit: 5) {
       id
       nombre
       estado_ciclo_vida
       geo_quality
       es_visitable
       horario_visitas
     }
   }
   ```

---

### Fase 2: Surveillance Engines

Una vez verificada la Fase 1, continuar con:

1. **ETL** - `lista_geografica_loader` (Carga masiva de OSM)
2. **Survey** - `SubsidyScraper` (Scrapers de subvenciones)
3. **Survey** - `ProcurementScraper` (Scraper de contratación pública)
4. **ETL** - `AutoMatcher` (Lógica de matching automático)

---

## 📊 Estructura de Archivos Modificados

```
sipi-core/
├── sipi/db/models/
│   ├── __init__.py          [MODIFICADO] - Exports OSMPlace, EventoHistorial
│   ├── osm.py               [NUEVO] - Modelo OSMPlace
│   ├── historial.py        [NUEVO] - Modelo EventoHistorial + TipoEventoHistorial
│   └── inmuebles.py         [MODIFICADO] - 5 campos nuevos + 2 ENUMs

sipi-api/
├── .env                     [MODIFICADO] - Credenciales Aiven
├── alembic/
│   ├── env.py               [MODIFICADO] - Soporte async + load_dotenv
│   └── versions/
│       └── 240ba0d4cbd7_*.py [NUEVO] - Migración Fase 1
└── app/graphql/
    └── schema.py            [MODIFICADO] - Carga modelos desde sipi-core

sipi-core/docs/agent_handoff/
├── task.md                  [MODIFICADO] - Fase 1 marcada como completada
└── PHASE1_COMPLETED.md      [NUEVO] - Este documento
```

---

## 🔍 Notas Técnicas

### Validación BIC + Visitable
- **Backend**: No hay validación automática. Los campos son opcionales en la DB.
- **Frontend**: Será el frontend quien valide que si `figura_proteccion == BIC` AND `es_visitable == true`, entonces se debe mostrar el campo `horario_visitas` como obligatorio en la UI.
- **Razón**: Flexibilidad. El dato puede no estar disponible inicialmente.

### Driver Asíncrono
- Se mantiene `asyncpg` en toda la stack (no psycopg síncrono).
- Alembic configurado con `create_async_engine()` y `asyncio.run()`.

### Schema PostgreSQL
- Todas las tablas se crean en el schema `sipi` (no `public`).
- La migración usa `schema='sipi'` explícitamente.

---

## ⚠️ Problemas Resueltos

### ✅ Schema Search Path para PostGIS
- **Problema**: asyncpg no encontraba el tipo `geometry` aunque PostGIS estaba habilitado
- **Causa**: PostGIS instalado en schema `public`, tablas SIPI en schema `sipi`
- **Solución**: Agregar `SET search_path TO sipi, portals, public` en las migraciones

### ✅ Consolidación de Migraciones
- **Problema**: Conflictos al separar migración inicial de migración Phase 1
- **Causa**: Los modelos ya incluían los campos de Phase 1, causando duplicación
- **Solución**: Consolidar en una única migración inicial (`240ba0d4cbd7`) que crea todo

### ✅ Extensiones de Supabase
- **Problema**: Necesidad de habilitar PostGIS y pgcrypto manualmente
- **Causa**: Supabase requiere activación explícita de extensiones desde el dashboard
- **Solución**: Habilitadas `postgis` (3.3.7) y `pgcrypto` (1.3) desde Supabase UI

---

## 👤 Autoría

**Implementado por**: Claude Sonnet 4.5
**Fecha**: 2025-12-21
**Sesión**: Phase 1 Implementation
