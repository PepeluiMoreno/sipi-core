# sipi-core/src/sipi/db/sessions/async_session.py
"""
Global async session maker for the SIPI application.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from .manager import AsyncDatabaseManager

# ================================================
# ENCONTRAR .env RELATIVO A ESTE ARCHIVO
# ================================================

# Este archivo: sipi-core/src/sipi/db/sessions/async_session.py
current_file = Path(__file__).resolve()

# Subir 5 niveles para llegar a la raíz de sipi-core
# sipi-core/src/sipi/db/sessions/async_session.py
#          ^    ^    ^   ^    ^
#          5    4    3   2    1  niveles para subir
sipi_core_root = current_file.parent.parent.parent.parent.parent

# Buscar .env en la raíz de sipi-core
env_path = sipi_core_root / '.env'

if env_path.exists():
    load_dotenv(env_path)

# Cargar .env específico del entorno (development/production)
environment = os.getenv("ENVIRONMENT", "development")
env_specific_path = sipi_core_root / f'.env.{environment}'

if env_specific_path.exists():
    load_dotenv(env_specific_path, override=True)

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Intentar construirla (sin schema en URL - asyncpg no lo soporta)
    user = os.getenv("POSTGRES_USER", "sipi")
    password = os.getenv("POSTGRES_PASSWORD", "sipi")
    host = os.getenv("POSTGRES_SERVICE_NAME", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "sipi")
    DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

# Schema se configura por separado (no como parámetro de URL)
DATABASE_SCHEMA = os.getenv("DATABASE_SCHEMA", "sipi")

# Create global database manager instance
db_manager = AsyncDatabaseManager(
    database_url=DATABASE_URL,
    echo=os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true",
    pool_size=int(os.getenv("POOL_SIZE", "20")),
    max_overflow=int(os.getenv("POOL_MAX_OVERFLOW", "10")),
)

# Export session maker for FastAPI dependencies
async_session_maker = db_manager.session_maker
get_session = db_manager.get_session

__all__ = ["async_session_maker", "get_session", "db_manager", "DATABASE_URL", "DATABASE_SCHEMA"]
