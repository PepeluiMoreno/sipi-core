from logging.config import fileConfig
import os
import sys
from pathlib import Path

from sqlalchemy import engine_from_config, pool, text
from alembic import context
from geoalchemy2 import alembic_helpers

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

sipi_core_root = Path(__file__).parent.parent
sys.path.insert(0, str(sipi_core_root / "src"))

# ---------------------------------------------------------
# MODELOS
# ---------------------------------------------------------

from db.models.base import AppBase, GISBase, APP_SCHEMA, GIS_SCHEMA
 

# Combine metadata from both schemas
from sqlalchemy import MetaData
combined_metadata = MetaData()

# Merge tables from both schemas
for table in AppBase.metadata.tables.values():
    table.to_metadata(combined_metadata)

for table in GISBase.metadata.tables.values():
    table.to_metadata(combined_metadata)

target_metadata = combined_metadata

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------
# ENV
# ---------------------------------------------------------

from dotenv import load_dotenv

env_path = sipi_core_root / ".env"
if env_path.exists():
    load_dotenv(env_path)

environment = os.getenv("ENVIRONMENT", "development")
env_specific_path = sipi_core_root / f".env.{environment}"
if env_specific_path.exists():
    load_dotenv(env_specific_path, override=True)

database_url = os.getenv("DATABASE_URL")

if not database_url:
    user = os.getenv("POSTGRES_USER", "sipi")
    password = os.getenv("POSTGRES_PASSWORD", "sipi")
    host = os.getenv("POSTGRES_SERVICE_NAME", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "sipi")
    database_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
else:
    database_url = database_url.replace(
        "postgresql+asyncpg://", "postgresql://"
    )

config.set_main_option("sqlalchemy.url", database_url)

# ---------------------------------------------------------
# MULTI-SCHEMA CONFIGURATION
# ---------------------------------------------------------

print(f"\n▶ Alembic Multi-Schema Configuration:")
print(f"  - APP Schema: {APP_SCHEMA}")
print(f"  - GIS Schema: {GIS_SCHEMA}")
print(f"  - Total tables in metadata: {len(combined_metadata.tables)}")

# Group tables by schema
app_tables = [t for t in combined_metadata.tables.values() if t.schema == APP_SCHEMA]
gis_tables = [t for t in combined_metadata.tables.values() if t.schema == GIS_SCHEMA]

print(f"\n▶ APP Schema tables ({len(app_tables)}):")
for t in app_tables:
    print(f"  - {t.schema}.{t.name}")

print(f"\n▶ GIS Schema tables ({len(gis_tables)}):")
for t in gis_tables:
    print(f"  - {t.schema}.{t.name}")

# ---------------------------------------------------------
# MULTI-SCHEMA FILTER (APP + GIS, EXCLUDE POSTGIS INTERNALS)
# ---------------------------------------------------------

def include_object(object, name, type_, reflected, compare_to):
    """
    Autogenerate for both APP and GIS schemas.
    Ignore PostGIS internal schemas (topology, tiger, etc).
    """
    
    # Schemas: only our application schemas
    if type_ == "schema":
        return name in (APP_SCHEMA, GIS_SCHEMA)
    
    # Tables: only from our schemas
    if type_ == "table":
        schema = getattr(object, "schema", None)
        return schema in (APP_SCHEMA, GIS_SCHEMA)
    
    # Indexes and constraints: only if table is ours
    if type_ in {
        "index",
        "unique_constraint",
        "foreign_key_constraint",
        "check_constraint",
    }:
        table = getattr(object, "table", None)
        if table is not None:
            return table.schema in (APP_SCHEMA, GIS_SCHEMA)
        return False
    
    # Columns: allow geometry ONLY if table is ours
    if type_ == "column":
        table = object.table
        return table.schema in (APP_SCHEMA, GIS_SCHEMA)
    
    return True

# ---------------------------------------------------------
# INIT DB (POSTGIS + SCHEMAS)
# ---------------------------------------------------------

def init_database(connection):
    """Initialize database with PostGIS and required schemas"""
    connection.execute(text("SELECT 1"))
    
    # Enable PostGIS extensions
    connection.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
    connection.execute(text("CREATE EXTENSION IF NOT EXISTS postgis_topology"))
    
    # Create both schemas
    connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {APP_SCHEMA}"))
    connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {GIS_SCHEMA}"))
    
    # Set search path to include both schemas
    connection.execute(
        text(f"SET search_path TO {APP_SCHEMA}, {GIS_SCHEMA}, public")
    )
    
    connection.commit()

# ---------------------------------------------------------
# MIGRATIONS OFFLINE
# ---------------------------------------------------------

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,            # ✅ MULTI-SCHEMA
        version_table_schema=APP_SCHEMA,  # Version table in APP schema
        include_object=include_object,
        process_revision_directives=alembic_helpers.writer,
        render_item=alembic_helpers.render_item,
        user_module_prefix="geoalchemy2.",
    )
    
    with context.begin_transaction():
        context.run_migrations()

# ---------------------------------------------------------
# MIGRATIONS ONLINE
# ---------------------------------------------------------

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    
    with connectable.connect() as connection:
        init_database(connection)
        
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,          # ✅ MULTI-SCHEMA
            version_table_schema=APP_SCHEMA,  # Version table in APP schema
            include_object=include_object,
            compare_type=True,
            compare_server_default=True,
            process_revision_directives=alembic_helpers.writer,
            render_item=alembic_helpers.render_item,
            user_module_prefix="geoalchemy2.",
        )
        
        with context.begin_transaction():
            context.run_migrations()

# ---------------------------------------------------------
# ENTRYPOINT
# ---------------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
