# Multi-Schema Architecture - Complete Implementation

## 🎯 Overview

This document provides a complete overview of the multi-schema architecture implementation for SIPI, including the separation of application and GIS models, and the reorganization of actor models into specialized modules.

## 📋 Quick Links

- **[Architecture Design](./MULTI_SCHEMA_ARCHITECTURE.md)** - Detailed design and rationale
- **[Implementation Summary](./IMPLEMENTATION_SUMMARY.md)** - What was implemented and how
- **[Migration Guide](./MIGRATION_GUIDE.md)** - Step-by-step migration instructions

## 🏗️ What Changed

### 1. Multi-Schema Database Architecture

**Before:**
- Single schema (`sipi` or `app`)
- Mixed business logic and geographic data
- Difficult to manage and optimize separately

**After:**
- **`app` schema**: Business domain models (actors, properties, documents, transactions)
- **`gis` schema**: Geographic/spatial data (administrative divisions, OSM data)
- Clear separation of concerns
- Independent optimization strategies

### 2. Actor Models Reorganization

**Before:**
- Single monolithic file: [`actores.py`](../src/sipi/db/models/actores.py) (298 lines)
- All actor types mixed together
- Difficult to navigate and maintain

**After:**
Organized into specialized modules:

```
src/sipi/db/models/actores/
├── __init__.py              # Package exports
├── _base.py                 # Base classes and mixins
├── notarios.py              # Notaries and notarial offices
├── registradores.py         # Property registrars and registries
├── administraciones.py      # Public administrations (all levels)
├── entidades_religiosas.py # Religious entities (dioceses, orders)
├── tecnicos.py              # Technical professionals
└── privados.py              # Private individuals and companies
```

### 3. Geographic Models Reorganization

**Before:**
- Mixed with application models
- Single schema
- No clear separation

**After:**
```
src/sipi/db/models/geografia/
├── __init__.py
└── divisiones.py            # ComunidadAutonoma, Provincia, Municipio
```

All in `gis` schema with cross-schema relationships to `app` models.

## 🚀 Key Features

### Multi-Schema Support

```python
from sipi.db.base import AppBase, GISBase

# Application models
class Notaria(AppBase):
    __tablename__ = "notarias"
    # Lives in 'app' schema

# Geographic models  
class Municipio(GISBase):
    __tablename__ = "municipios"
    # Lives in 'gis' schema
```

### Cross-Schema Relationships

```python
# Foreign key from APP to GIS schema
municipio_id: Mapped[str] = mapped_column(
    String(36), 
    ForeignKey("gis.municipios.id"),  # Explicit schema reference
    index=True
)

# Relationship works transparently
municipio: Mapped["Municipio"] = relationship("Municipio")
```

### Improved Domain Design

Each actor type now has:
- ✅ Dedicated module
- ✅ Comprehensive documentation
- ✅ Clear responsibilities
- ✅ Type safety
- ✅ Explicit relationships

## 📁 File Structure

### Created Files

```
docs/
├── MULTI_SCHEMA_ARCHITECTURE.md    # Architecture design
├── IMPLEMENTATION_SUMMARY.md       # Implementation details
├── MIGRATION_GUIDE.md              # Migration instructions
└── MULTI_SCHEMA_README.md          # This file

src/sipi/db/models/
├── actores/                        # Actor models package
│   ├── __init__.py
│   ├── _base.py
│   ├── notarios.py
│   ├── registradores.py
│   ├── administraciones.py
│   ├── entidades_religiosas.py
│   ├── tecnicos.py
│   └── privados.py
└── geografia/                      # Geographic models package
    ├── __init__.py
    └── divisiones.py
```

### Modified Files

```
src/sipi/db/
├── base.py                         # Added AppBase, GISBase
└── models/__init__.py              # Updated imports

alembic/
└── env.py                          # Multi-schema support
```

## 🔧 Configuration

### Environment Variables

```bash
# Application schema (default: "app")
DATABASE_SCHEMA=app

# GIS schema (default: "gis")  
GIS_SCHEMA=gis

# Database connection
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

### Database Setup

The system automatically:
1. Creates both schemas (`app` and `gis`)
2. Enables PostGIS extensions
3. Sets search path: `app, gis, public`
4. Manages cross-schema foreign keys

## 📊 Benefits

### Maintainability
- **Smaller files**: Each file has single responsibility
- **Easier navigation**: Find models by domain/type
- **Reduced complexity**: No more monolithic files

### Scalability
- **Independent evolution**: Schemas evolve separately
- **Easier testing**: Test domains in isolation
- **Better performance**: Separate optimization per schema

### Clarity
- **Clear boundaries**: Business logic vs. geographic data
- **Explicit dependencies**: Cross-schema relationships obvious
- **Better documentation**: Self-documenting modules

### Safety
- **Type safety**: Full type hints throughout
- **Schema isolation**: Prevents cross-contamination
- **Migration control**: Alembic manages both schemas

## 🎓 Usage Examples

### Importing Models

```python
# Import from main package
from sipi.models import Notaria, Municipio, Administracion

# Or import from subpackages
from sipi.models.actores import Notaria, Administracion
from sipi.models.geografia import Municipio
```

### Querying Across Schemas

```python
from sqlalchemy import select
from sipi.models import Notaria, Municipio

# Cross-schema join works transparently
query = (
    select(Notaria)
    .join(Municipio)
    .where(Municipio.nombre_oficial == 'Madrid')
)

# Execute query
async with get_session() as session:
    result = await session.execute(query)
    notarias = result.scalars().all()
```

### Creating New Models

```python
from sipi.db.base import AppBase  # For business models
from sipi.db.base import GISBase  # For geographic models
from sipi.mixins import UUIDPKMixin, AuditMixin

# Business model (APP schema)
class MyBusinessModel(UUIDPKMixin, AuditMixin, AppBase):
    __tablename__ = "my_table"
    # Fields...

# Geographic model (GIS schema)
class MyGeoModel(UUIDPKMixin, AuditMixin, GISBase):
    __tablename__ = "my_geo_table"
    # Fields...
```

## 🧪 Testing

### Verify Installation

```bash
# Test imports
python -c "from sipi.models import Notaria, Municipio; print('✓ OK')"

# Test base classes
python -c "from sipi.db.base import AppBase, GISBase; print('✓ OK')"

# Check schemas
python -c "from sipi.db.base import APP_SCHEMA, GIS_SCHEMA; print(f'APP: {APP_SCHEMA}, GIS: {GIS_SCHEMA}')"
```

### Generate Migration

```bash
# Generate migration
alembic revision --autogenerate -m "multi_schema_architecture"

# Review migration
cat alembic/versions/<generated_file>.py

# Apply migration
alembic upgrade head
```

### Verify Database

```sql
-- Check schemas exist
\dn

-- Check tables in APP schema
\dt app.*

-- Check tables in GIS schema
\dt gis.*

-- Check cross-schema foreign keys
SELECT 
    tc.table_schema, 
    tc.table_name,
    ccu.table_schema AS foreign_schema,
    ccu.table_name AS foreign_table
FROM information_schema.table_constraints tc
JOIN information_schema.constraint_column_usage ccu
  ON tc.constraint_name = ccu.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema IN ('app', 'gis');
```

## 📝 Next Steps

1. **Review Documentation**
   - Read [Architecture Design](./MULTI_SCHEMA_ARCHITECTURE.md)
   - Read [Implementation Summary](./IMPLEMENTATION_SUMMARY.md)

2. **Plan Migration**
   - Review [Migration Guide](./MIGRATION_GUIDE.md)
   - Backup your database
   - Test on development environment

3. **Generate Migration**
   ```bash
   alembic revision --autogenerate -m "multi_schema_architecture"
   ```

4. **Test Migration**
   - Apply to development database
   - Verify data integrity
   - Test application functionality

5. **Deploy to Production**
   - Follow migration guide
   - Monitor for issues
   - Have rollback plan ready

## 🆘 Troubleshooting

### Common Issues

**Import Errors**
```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
pip install -e .
```

**Schema Not Found**
```sql
CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS gis;
```

**Foreign Key Errors**
```sql
-- Check for orphaned records
SELECT * FROM app.notarias n
LEFT JOIN gis.municipios m ON n.municipio_id = m.id
WHERE n.municipio_id IS NOT NULL AND m.id IS NULL;
```

See [Migration Guide](./MIGRATION_GUIDE.md) for detailed troubleshooting.

## 📚 Additional Resources

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL Schemas](https://www.postgresql.org/docs/current/ddl-schemas.html)
- [PostGIS Documentation](https://postgis.net/documentation/)

## 👥 Support

For questions or issues:
1. Check the [Migration Guide](./MIGRATION_GUIDE.md) troubleshooting section
2. Review [Implementation Summary](./IMPLEMENTATION_SUMMARY.md)
3. Contact the development team

## ✅ Checklist

Before deploying:
- [ ] Read all documentation
- [ ] Backup database
- [ ] Test on development environment
- [ ] Review generated migration
- [ ] Verify foreign keys
- [ ] Test application functionality
- [ ] Update deployment scripts
- [ ] Notify team
- [ ] Have rollback plan ready

## 🎉 Summary

The multi-schema architecture provides:
- ✅ Clear separation between business and geographic data
- ✅ Organized actor models by type
- ✅ Improved maintainability and scalability
- ✅ Better documentation and type safety
- ✅ Full Alembic migration support
- ✅ Backward compatibility
- ✅ Production-ready implementation

The system is now ready for migration and deployment!
