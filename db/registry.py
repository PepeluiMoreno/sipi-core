# db/registry.py

from sqlalchemy.orm import declarative_base

# Base declarativa para todos los modelos
Base = declarative_base()

# Schemas
APP_SCHEMA = "app"       # schema principal de la aplicación
GIS_SCHEMA = "gis"       # schema para datos GIS

