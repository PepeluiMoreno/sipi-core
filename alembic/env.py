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

from sipi.db.base import Base
from sipi.db import models  # noqa: F401  (importa TODOS los modelos)

target_metadata = Base.metadata

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
# SCHEMA
# ---------------------------------------------------------

SCHEMA = getattr(Base, "schema", None) or os.getenv("DATABASE_SCHEMA", "sipi")

print(f"\n▶ Alembic schema activo: {SCHEMA}")
print(f"▶ Tablas en metadata: {len(Base.metadata.tables)}")
for t in Base.metadata.tables.values():
    print(f"  - {t.schema}.{t.name}")

# ---------------------------------------------------------
# FILTRO CLAVE (MULTI-SCHEMA + POSTGIS)
# ---------------------------------------------------------

def include_object(object, name, type_, reflected, compare_to):
    """
    Autogenerar SOLO para el schema de la aplicación.
    Ignorar completamente schemas externos (PostGIS, public, etc).
    """

    # Schemas: solo el nuestro
    if type_ == "schema":
        return name == SCHEMA

    # Tablas: solo las del schema de la app
    if type_ == "table":
        return getattr(object, "schema", None) == SCHEMA

    # Índices y constraints: solo si la tabla es nuestra
    if type_ in {
        "index",
        "unique_constraint",
        "foreign_key_constraint",
        "check_constraint",
    }:
        table = getattr(object, "table", None)
        if table is not None:
            return table.schema == SCHEMA
        return False

    # Columnas: permitir geometry SOLO si la tabla es nuestra
    if type_ == "column":
        table = object.table
        return table.schema == SCHEMA

    return True

# ---------------------------------------------------------
# INIT DB (POSTGIS + SCHEMA)
# ---------------------------------------------------------

def init_database(connection):
    connection.execute(text("SELECT 1"))

    connection.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
    connection.execute(text("CREATE EXTENSION IF NOT EXISTS postgis_topology"))

    connection.execute(
        text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
    )

    connection.execute(
        text(f"SET search_path TO {SCHEMA}, public")
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
        include_schemas=True,            # ✅ CLAVE
        version_table_schema=SCHEMA,
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
            include_schemas=True,          # ✅ CLAVE
            version_table_schema=SCHEMA,
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
