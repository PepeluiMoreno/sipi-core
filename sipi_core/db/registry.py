# db/registry.py

import os
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

# Schemas de la aplicación (donde van las tablas)
APP_SCHEMA = os.getenv("APP_SCHEMA", "app")
GIS_SCHEMA = os.getenv("GIS_SCHEMA", "gis")

# Schema por defecto para Base
DEFAULT_SCHEMA = os.getenv("DEFAULT_SCHEMA", APP_SCHEMA)

# Metadata con schema por defecto
metadata = MetaData(schema=DEFAULT_SCHEMA)
Base = declarative_base(metadata=metadata)
