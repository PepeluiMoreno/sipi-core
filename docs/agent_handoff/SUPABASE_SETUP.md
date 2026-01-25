# Configuración de Supabase para SIPI

**Fecha**: 2025-12-21
**Provider**: Supabase (PostgreSQL DBaaS)

---

## Por qué usar schema `sipi` en lugar de `public`

### Ventajas de usar un schema dedicado

#### 1. Organización y Namespacing
- Separa claramente las tablas del proyecto SIPI de otras aplicaciones que puedan compartir la misma base de datos
- Evita conflictos de nombres con otras aplicaciones
- Facilita la gestión multi-tenant si en el futuro necesitas múltiples instancias

#### 2. Seguridad
- Puedes aplicar permisos específicos a nivel de schema
- Ejemplo: Un usuario puede tener acceso de solo lectura al schema `sipi` pero no a `public`
- Facilita la creación de roles específicos para diferentes componentes del sistema

#### 3. Separación de Concerns
En el proyecto SIPI se usan dos schemas:
- **`sipi`**: Datos del core del sistema (Inmuebles, OSMPlaces, Lifecycle)
- **`portals`**: Datos de staging/discovery (anuncios scrapeados, detecciones pendientes de validación)

Esta separación lógica hace que sea más claro qué datos son "oficiales" (sipi) y cuáles son "en proceso de validación" (portals).

#### 4. Mantenimiento
- Puedes hacer backup selectivo por schema
- Puedes hacer `DROP SCHEMA sipi CASCADE` sin afectar otras aplicaciones
- Facilita migraciones futuras o replicación parcial

#### 5. Compatibilidad con Supabase
- Supabase usa `public` para sus propias tablas de autenticación, storage, etc.
- Usar un schema propio evita mezclar tus tablas con las de Supabase

---

## Configuración Actual

### Extensiones Habilitadas

Las siguientes extensiones están habilitadas en el dashboard de Supabase:

1. **postgis** (3.3.7)
   - Ubicación: schema `public`
   - Propósito: Tipos geometry/geography para datos espaciales
   - Usado en: `osm_places.geom`, `inmuebles_raw.geom`

2. **pgcrypto** (1.3)
   - Ubicación: schema `extensions`
   - Propósito: Función `gen_random_uuid()` para UUIDs
   - Usado en: Todas las tablas con PK tipo UUID

### Connection Strings

```env
# Direct connection (para migraciones)
DATABASE_URL=postgresql+asyncpg://postgres.edgrrunsbyhutbceafuf:jO04ufJ7R06LWRLE@aws-1-eu-west-1.pooler.supabase.com:5432/postgres

# Pooled connection (para aplicación en producción)
DATABASE_URL_POOLED=postgresql+asyncpg://postgres.edgrrunsbyhutbceafuf:jO04ufJ7R06LWRLE@aws-1-eu-west-1.pooler.supabase.com:6543/postgres
```

**Nota**: Actualmente se usa la conexión directa (puerto 5432) para todo. La conexión pooled (puerto 6543) está disponible para cuando sea necesario escalar.

---

## Search Path

Para que las tablas en `sipi` puedan usar tipos de PostGIS (que están en `public`), las migraciones configuran el search path:

```sql
SET search_path TO sipi, portals, public;
```

Esto permite que:
- Las tablas se creen en `sipi` (primer schema en el path)
- Los tipos `geometry`, `geography` se encuentren en `public`
- Las funciones como `ST_Distance` estén disponibles

---

## Cómo habilitar extensiones en Supabase

1. Ir al dashboard de Supabase: https://supabase.com/dashboard
2. Seleccionar tu proyecto
3. Navegar a: **Database** → **Extensions**
4. Buscar la extensión deseada
5. Click en el toggle para habilitarla

### Extensiones requeridas para SIPI:
- ✅ `postgis` - Ya habilitada
- ✅ `pgcrypto` - Ya habilitada

---

## Scripts de Utilidad

### Reset completo de la base de datos

```bash
cd sipi-api
python reset_db.py
```

Este script:
- Elimina schemas `sipi` y `portals` con CASCADE
- Elimina todos los tipos ENUM
- Elimina la tabla `alembic_version`

**ADVERTENCIA**: Esto borrará TODOS los datos. Úsalo solo en desarrollo.

### Aplicar migraciones

```bash
cd sipi-api
alembic upgrade head
```

### Verificar estado de migraciones

```bash
cd sipi-api
alembic current
```

### Ver historial de migraciones

```bash
cd sipi-api
alembic history
```

---

## Troubleshooting

### Error: "type geometry does not exist"

**Causa**: El search_path no incluye el schema `public` donde está PostGIS.

**Solución**: Asegurarse de que la migración incluye:
```python
op.execute(text("SET search_path TO sipi, portals, public"))
```

### Error: "schema sipi does not exist"

**Causa**: La migración intentó crear tablas antes de crear el schema.

**Solución**: La migración actual ya crea los schemas correctamente en el orden adecuado.

### Error: "permission denied for schema sipi"

**Causa**: El usuario de Supabase no tiene permisos en el schema.

**Solución**: El usuario `postgres.edgrrunsbyhutbceafuf` es el owner, tiene todos los permisos.

---

## Estado Actual

- ✅ Schemas `sipi` y `portals` creados
- ✅ 51 tablas creadas en `sipi`
- ✅ PostGIS funcionando correctamente
- ✅ Migración `240ba0d4cbd7` aplicada
- ✅ Todos los modelos de Phase 1 disponibles

---

## Próximos Pasos

1. Probar la API GraphQL con los nuevos modelos
2. Implementar Phase 2: Surveillance Engines
3. Considerar habilitar extensiones adicionales si son necesarias:
   - `pg_trgm` - Para búsqueda fuzzy de texto
   - `unaccent` - Para búsqueda sin acentos
   - `pg_stat_statements` - Para análisis de performance
