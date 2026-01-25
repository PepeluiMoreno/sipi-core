# Próximos Pasos - Phase 1 → Phase 2

**Estado Actual**: Phase 1 completada, esperando activación de base de datos Aiven.

---

## 🔴 ACCIÓN INMEDIATA (Cuando DB esté activa)

### 1. Aplicar Migración de Base de Datos

```bash
cd /path/to/sipi-api

# Verificar estado actual de migraciones
alembic current

# Ver migraciones pendientes
alembic history

# Aplicar migración Phase 1
alembic upgrade head

# Verificar que se aplicó correctamente
alembic current
```

**Esperado**: Debe mostrar `240ba0d4cbd7 (head)` como la revisión actual.

---

### 2. Verificar Tablas Creadas

Conectar a la base de datos y ejecutar:

```sql
-- Listar todas las tablas del schema sipi
\dt sipi.*

-- Debe mostrar (entre otras):
-- sipi.osm_places
-- sipi.inmueble_lifecycle
-- sipi.inmuebles (con campos nuevos)

-- Verificar estructura de osm_places
\d sipi.osm_places

-- Verificar estructura de inmueble_lifecycle
\d sipi.inmueble_lifecycle

-- Verificar que inmuebles tiene los nuevos campos
\d sipi.inmuebles
-- Buscar: estado_ciclo_vida, geo_quality, es_visitable, horario_visitas, enlace_web_visitas

-- Verificar ENUMs creados
\dT+ estadociclovida
\dT+ geoquality
\dT+ lifecycleeventtype
```

---

### 3. Probar GraphQL API

```bash
cd /path/to/sipi-api

# Iniciar servidor
uvicorn app.graphql.app:application --reload --port 8040
```

Abrir en navegador: `http://localhost:8040/graphql`

**Query de prueba 1** - Verificar campos nuevos en Inmueble:
```graphql
query TestInmuebleFields {
  inmuebles(limit: 5) {
    id
    nombre
    estado_ciclo_vida
    geo_quality
    es_visitable
    horario_visitas
    enlace_web_visitas
  }
}
```

**Query de prueba 2** - Listar OSMPlaces (vacío inicialmente):
```graphql
query TestOSMPlaces {
  osmPlaces(limit: 10) {
    id
    osm_id
    name
    amenity
    geom
  }
}
```

**Query de prueba 3** - Listar Lifecycle events (vacío inicialmente):
```graphql
query TestLifecycle {
  inmuebleLifecycles(limit: 10) {
    id
    inmueble_id
    event_type
    event_date
    description
    source
  }
}
```

**Mutation de prueba** - Crear evento de lifecycle:
```graphql
mutation TestCreateLifecycleEvent {
  createInmuebleLifecycle(data: {
    inmueble_id: "REPLACE_WITH_REAL_ID"
    event_type: "alta_inmatriculacion"
    event_date: "2025-12-21T12:00:00"
    description: "Prueba de registro inicial"
    source: "Manual"
  }) {
    id
    event_type
    event_date
    description
  }
}
```

---

## ✅ Checklist de Verificación

- [ ] Migración aplicada sin errores
- [ ] Tabla `sipi.osm_places` existe
- [ ] Tabla `sipi.inmueble_lifecycle` existe
- [ ] Tabla `sipi.inmuebles` tiene 5 campos nuevos
- [ ] 3 ENUMs creados correctamente
- [ ] GraphQL expone tipo `OSMPlace`
- [ ] GraphQL expone tipo `InmuebleLifecycle`
- [ ] GraphQL expone campos nuevos en `Inmueble`
- [ ] Mutation `createOSMPlace` funciona
- [ ] Mutation `createInmuebleLifecycle` funciona

---

## 🚀 Continuar con Phase 2

Una vez verificado todo lo anterior, proceder con:

### Phase 2: Surveillance Engines

Ver [task.md](task.md) - Tasks ID: 12-15

#### Tarea 12: OSM Census Loader
**Objetivo**: Script ETL para cargar censo de lugares desde OpenStreetMap.

**Ubicación**: `sipi-survey/pipelines/osm_census_loader.py`

**Funcionalidad**:
- Extraer lugares religiosos/patrimoniales de OSM usando Overpass API
- Normalizar datos (municipio, coordenadas)
- Guardar en tabla `osm_places`

**Entradas**:
- Bounding box (España o región específica)
- Filtros OSM (amenity=place_of_worship, historic=*, etc.)

**Salidas**:
- Registros en `sipi.osm_places`
- Log de registros insertados/actualizados

---

#### Tarea 13: Subsidy Scraper
**Objetivo**: Scraper de subvenciones públicas para inmuebles (NIF que empiezan con 'R%').

**Ubicación**: `sipi-survey/src/modules/subsidies/`

**Fuentes**:
- Base de Datos Nacional de Subvenciones (BDNS)
- BOE (Boletín Oficial del Estado)
- Boletines autonómicos

**Funcionalidad**:
- Buscar convocatorias de subvenciones para rehabilitación/restauración
- Filtrar por NIF de entidades religiosas (R%)
- Extraer: NIF beneficiario, importe, fecha, descripción

**Salidas**:
- Crear evento `REHABILITACION_SUBVENCIONADA` en `inmueble_lifecycle`
- Actualizar campo `details` con JSON de la subvención

---

#### Tarea 14: Procurement Scraper
**Objetivo**: Scraper de contratación pública (obras, servicios en inmuebles).

**Ubicación**: `sipi-survey/src/modules/procurement/`

**Fuentes**:
- Plataforma de Contratación del Sector Público
- Contratos menores de ayuntamientos

**Funcionalidad**:
- Buscar contratos relacionados con inmuebles patrimoniales
- Filtrar por tipo (obras, restauración, mantenimiento)
- Extraer: licitador, importe, fecha, descripción

**Salidas**:
- Crear evento `REHABILITACION` en `inmueble_lifecycle`
- Actualizar campo `details` con JSON del contrato

---

#### Tarea 15: AutoMatcher Pipeline
**Objetivo**: Lógica de matching automático entre anuncios/subvenciones y censo de inmuebles.

**Ubicación**: `sipi-survey/pipelines/auto_matcher.py`

**Funcionalidad**:
1. **Geolocalización**: Comparar coordenadas de anuncio con `osm_places`
2. **Nombre**: Fuzzy matching de nombres (Levenshtein distance)
3. **Score de confianza**: 0-1 (threshold: 0.8 para auto-match)
4. **Acciones**:
   - Score > 0.8: Auto-vincular + crear evento lifecycle
   - Score 0.5-0.8: Marcar para revisión manual (GeoMatcher UI)
   - Score < 0.5: Descartar

**Salidas**:
- Actualizaciones en `estado_ciclo_vida` de `inmuebles`
- Eventos en `inmueble_lifecycle`
- Registros en `deteccion_anuncio` (tabla Discovery existente)

---

## 📊 Métricas de Éxito Phase 2

Al finalizar Phase 2, el sistema debe:

- [ ] Tener al menos 1,000 lugares cargados en `osm_places`
- [ ] Detectar automáticamente subvenciones semanalmente
- [ ] Crear eventos de lifecycle automáticamente
- [ ] Tener >70% de auto-matching exitoso (score > 0.8)
- [ ] <30% de detecciones requieren validación manual

---

## 🔗 Referencias

- [Phase 1 Complete](PHASE1_COMPLETED.md)
- [Implementation Plan](implementation_plan.md)
- [Task List](task.md)
