# sipi-core/config.py
"""
Configuracion centralizada SIPI.
Todos los componentes importan desde aqui.

Uso:
  - Establecer ENVIRONMENT=development o ENVIRONMENT=production
  - Se cargara automaticamente .env.development o .env.production
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Dict
from dotenv import load_dotenv

# Rutas base
CONFIG_DIR = Path(__file__).parent.resolve()
WORKSPACE_ROOT = CONFIG_DIR.parent

# Cargar configuracion una sola vez
_loaded = False


def _load():
    global _loaded
    if _loaded:
        return

    # Determinar entorno: variable de sistema > .env base
    env = os.getenv("ENVIRONMENT")

    if not env:
        # Intentar cargar .env base para obtener ENVIRONMENT
        base_env = CONFIG_DIR / ".env"
        if base_env.exists():
            load_dotenv(dotenv_path=base_env)
            env = os.getenv("ENVIRONMENT", "development")
        else:
            env = "development"

    # Seleccionar archivo segun entorno
    env_file = CONFIG_DIR / f".env.{env}"

    if not env_file.exists():
        raise FileNotFoundError(f"Archivo de configuracion no encontrado: {env_file}")

    # Cargar archivo de entorno
    load_dotenv(dotenv_path=env_file, override=True)
    os.environ["ENVIRONMENT"] = env

    _loaded = True


@dataclass(frozen=True)
class Config:
    """Configuracion del proyecto SIPI"""

    def __post_init__(self):
        _load()

    # Base de datos
    @property
    def DATABASE_URL(self) -> str:
        return os.getenv("DATABASE_URL", "")

    @property
    def DATABASE_SCHEMA(self) -> str:
        return os.getenv("DATABASE_SCHEMA", "sipi")

    # API Backend
    @property
    def API_HOST(self) -> str:
        return os.getenv("API_HOST", "0.0.0.0")

    @property
    def API_PORT(self) -> int:
        return int(os.getenv("API_PORT", "8040"))

    @property
    def API_URL(self) -> str:
        return os.getenv("API_URL", f"http://{self.API_HOST}:{self.API_PORT}/graphql")

    # SQLAlchemy
    @property
    def SQLALCHEMY_ECHO(self) -> bool:
        return os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"

    @property
    def POOL_SIZE(self) -> int:
        return int(os.getenv("POOL_SIZE", "20"))

    @property
    def POOL_MAX_OVERFLOW(self) -> int:
        return int(os.getenv("POOL_MAX_OVERFLOW", "10"))

    @property
    def POOL_TIMEOUT(self) -> int:
        return int(os.getenv("POOL_TIMEOUT", "30"))

    # Entorno
    @property
    def ENVIRONMENT(self) -> str:
        return os.getenv("ENVIRONMENT", "development")

    @property
    def DEBUG(self) -> bool:
        return self.ENVIRONMENT == "development"

    # Rutas del proyecto
    @property
    def PATHS(self) -> Dict[str, Path]:
        return {
            "core": CONFIG_DIR,
            "api": WORKSPACE_ROOT / "sipi-api",
            "frontend": WORKSPACE_ROOT / "sipi-frontend",
        }


# Instancia global
CONFIG = Config()


# Funciones de conveniencia
def get_db_url() -> str:
    return CONFIG.DATABASE_URL

def get_db_schema() -> str:
    return CONFIG.DATABASE_SCHEMA

def get_api_url() -> str:
    return CONFIG.API_URL


if __name__ == "__main__":
    _load()
    print(f"ENVIRONMENT: {CONFIG.ENVIRONMENT}")
    print(f"DATABASE_URL: {CONFIG.DATABASE_URL[:50]}...")
    print(f"DATABASE_SCHEMA: {CONFIG.DATABASE_SCHEMA}")
    print(f"API: {CONFIG.API_HOST}:{CONFIG.API_PORT}")
