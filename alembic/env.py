# alembic/env.py

from logging.config import fileConfig
import sys
from pathlib import Path
from collections import defaultdict
from alembic import context
from geoalchemy2 import alembic_helpers

# ---------------------------------------------------------
# PATHS (estructura aplanada)
# ---------------------------------------------------------
sipi_core_root = Path(__file__).parent.parent
sys.path.insert(0, str(sipi_core_root))

# ---------------------------------------------------------
# IMPORT MODELS (CRÍTICO - registra todas las tablas en metadata)
# ---------------------------------------------------------
from models import *

# ---------------------------------------------------------
# IMPORT METADATA Y MANAGER
# ---------------------------------------------------------
from db.metadata import get_combined_metadata, ALEMBIC_SCHEMAS
from db.sessions.manager import SyncDatabaseManager, DatabaseConfig

# ---------------------------------------------------------
# CONFIGURACIÓN ALEMBIC
# ---------------------------------------------------------
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------
# METADATA Y RESUMEN POR SCHEMA
# ---------------------------------------------------------
target_metadata = get_combined_metadata()

# Contar tablas por schema (no listarlas)
tables_by_schema = defaultdict(int)
for table_name, table in target_metadata.tables.items():
    schema = getattr(table, "schema", None) or "default"
    tables_by_schema[schema] += 1

print(f"Alembic managing schemas: {ALEMBIC_SCHEMAS}")
print("Tables in target_metadata for Alembic:")
for schema in ALEMBIC_SCHEMAS:
    count = tables_by_schema.get(schema, 0)
    print(f"  - {schema}: {count} tables")
total = sum(tables_by_schema.values())
print(f"  Total: {total} tables")

# ---------------------------------------------------------
# FILTRO DE OBJETOS (corregido)
# ---------------------------------------------------------
def include_object(object, name, type_, reflected, compare_to):
    """
    Incluye solo tablas de nuestros schemas definidos, ignora PostGIS internos
    """
    if type_ == "schema":
        return name in ALEMBIC_SCHEMAS
    
    if type_ == "table":
        schema = getattr(object, "schema", None)
        return schema in ALEMBIC_SCHEMAS
    
    if type_ in {"index", "unique_constraint", "foreign_key_constraint", "check_constraint"}:
        table = getattr(object, "table", None)
        if table is not None:
            schema = getattr(table, "schema", None)
            return schema in ALEMBIC_SCHEMAS
        return False
    
    if type_ == "column":
        table = getattr(object, "table", None)
        if table is not None:
            schema = getattr(table, "schema", None)
            return schema in ALEMBIC_SCHEMAS
        return False
    
    return True

# ---------------------------------------------------------
# MIGRACIONES
# ---------------------------------------------------------
def run_migrations_offline():
    """Modo offline: genera archivos de migración sin conectar a BD"""
    url = DatabaseConfig.get_database_url(async_mode=False)
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        version_table_schema=ALEMBIC_SCHEMAS[0],
        include_object=include_object,
        process_revision_directives=alembic_helpers.writer,
        render_item=alembic_helpers.render_item,
        user_module_prefix="geoalchemy2.",
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Modo online: ejecuta migraciones conectándose a la BD"""
    manager = SyncDatabaseManager(echo=False)
    
    try:
        manager.init_database()
        
        with manager.engine.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                include_schemas=True,
                version_table_schema=ALEMBIC_SCHEMAS[0],
                include_object=include_object,
                compare_type=True,
                compare_server_default=True,
                process_revision_directives=alembic_helpers.writer,
                render_item=alembic_helpers.render_item,
                user_module_prefix="geoalchemy2.",
            )
            with context.begin_transaction():
                context.run_migrations()
    finally:
        manager.close()


# ---------------------------------------------------------
# ENTRYPOINT
# ---------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()