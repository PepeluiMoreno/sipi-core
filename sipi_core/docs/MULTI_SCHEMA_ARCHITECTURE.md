# Multi-Schema Architecture Design

## Overview

This document describes the multi-schema architecture for SIPI, separating application domain models from GIS/spatial data.

## Schema Separation

### `app` Schema (Application Domain)
Contains all business logic and domain models:

- **Actors**: People and organizations (notaries, registrars, technicians, administrations, etc.)
- **Properties**: Real estate properties and their attributes
- **Documents**: Legal and administrative documents
- **Transactions**: Property transmissions and interventions
- **Typologies**: Reference data and catalogs
- **Users**: Application users and roles

### `gis` Schema (Geographic Information System)
Contains spatial and geographic data:

- **Geographic Entities**: Administrative divisions (comunidades, provincias, municipios)
- **Spatial Data**: Geometries, coordinates, spatial indexes
- **OSM Integration**: OpenStreetMap data and mappings
- **Spatial Queries**: PostGIS-specific tables and functions

## Benefits

1. **Clear Separation of Concerns**: Business logic separated from geographic data
2. **Independent Evolution**: Schemas can evolve independently
3. **Better Performance**: Separate indexes and optimization strategies
4. **Easier Maintenance**: Clearer organization and responsibilities
5. **Migration Safety**: Alembic can manage schemas independently
6. **Security**: Different access controls per schema

## Implementation Strategy

### Phase 1: Base Classes
- Create `AppBase` for application models (schema: `app`)
- Create `GISBase` for geographic models (schema: `gis`)
- Keep existing `Base` as alias to `AppBase` for backward compatibility

### Phase 2: Model Reorganization
- Move geographic models to `gis` schema
- Split `actores.py` into specialized modules:
  - `notarios.py`: Notaries and notarial offices
  - `registradores.py`: Property registrars and registries
  - `administraciones.py`: Public administrations
  - `entidades_religiosas.py`: Religious entities (dioceses, orders)
  - `tecnicos.py`: Technical professionals
  - `privados.py`: Private individuals and companies

### Phase 3: Alembic Configuration
- Update `alembic/env.py` to handle multiple schemas
- Configure separate version tables per schema
- Implement schema-aware migration filters

### Phase 4: Migration
- Create migration to move GIS tables to `gis` schema
- Update foreign key references
- Verify data integrity

## Model Organization

### Application Models (`app` schema)

```
src/sipi/db/models/
├── actores/
│   ├── __init__.py
│   ├── notarios.py          # Notaria, NotariaTitular
│   ├── registradores.py     # RegistroPropiedad, RegistroPropiedadTitular
│   ├── administraciones.py  # Administracion, AdministracionTitular
│   ├── entidades_religiosas.py  # Diocesis, EntidadReligiosa, etc.
│   ├── tecnicos.py          # Tecnico, ColegioProfesional
│   └── privados.py          # Privado, AgenciaInmobiliaria
├── inmuebles.py
├── documentos.py
├── transmisiones.py
├── intervenciones.py
├── subvenciones.py
├── tipologias.py
├── users.py
└── discovery.py
```

### Geographic Models (`gis` schema)

```
src/sipi/db/models/
├── geografia/
│   ├── __init__.py
│   ├── divisiones.py        # ComunidadAutonoma, Provincia, Municipio
│   └── osm.py               # OSMPlace, spatial data
```

## Foreign Key Relationships

Cross-schema foreign keys are supported in PostgreSQL:

```python
# In app schema model
municipio_id: Mapped[str] = mapped_column(
    String(36), 
    ForeignKey("app.gis.municipios.id"),
    index=True
)
```

## Alembic Multi-Schema Configuration

```python
# alembic/env.py
APP_SCHEMA = "app"
GIS_SCHEMA = "gis"

def include_object(object, name, type_, reflected, compare_to):
    """Filter objects by schema"""
    if type_ == "schema":
        return name in (APP_SCHEMA, GIS_SCHEMA)
    
    if type_ == "table":
        schema = getattr(object, "schema", None)
        return schema in (APP_SCHEMA, GIS_SCHEMA)
    
    # ... handle other types
```

## Migration Strategy

1. **Create GIS schema**: `CREATE SCHEMA IF NOT EXISTS gis`
2. **Move geographic tables**: 
   - `ALTER TABLE app.comunidades_autonomas SET SCHEMA gis`
   - `ALTER TABLE app.provincias SET SCHEMA gis`
   - `ALTER TABLE app.municipios SET SCHEMA gis`
3. **Update foreign keys**: Automatically handled by PostgreSQL
4. **Update search_path**: `SET search_path TO app, gis, public`

## Testing Strategy

1. Verify schema creation
2. Test cross-schema foreign keys
3. Validate spatial queries
4. Check Alembic autogenerate
5. Test rollback scenarios

## Rollback Plan

If issues arise:
1. Keep backup of current schema
2. Use Alembic downgrade
3. Restore from backup if needed
4. Document lessons learned
