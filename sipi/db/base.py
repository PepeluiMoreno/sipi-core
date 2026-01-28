# app/db/base.py
"""
Multi-Schema Base Classes for SIPI

This module provides separate base classes for application and GIS models,
enabling clear separation of concerns and independent schema management.
"""

import os
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

# ---------------------------------------------------------
# SCHEMA CONFIGURATION
# ---------------------------------------------------------

APP_SCHEMA = (
    os.getenv("DATABASE_SCHEMA")
    or os.getenv("DB_SCHEMA")
    or "app"
)

GIS_SCHEMA = (
    os.getenv("GIS_SCHEMA")
    or "gis"
)

# ---------------------------------------------------------
# METADATA FOR EACH SCHEMA
# ---------------------------------------------------------

app_metadata = MetaData(schema=APP_SCHEMA)
gis_metadata = MetaData(schema=GIS_SCHEMA)

# ---------------------------------------------------------
# APPLICATION BASE (Business Domain Models)
# ---------------------------------------------------------

class AppBase(DeclarativeBase):
    """
    Base ORM for application domain models.
    
    - All business logic tables (actors, properties, documents, etc.)
    - Lives in APP_SCHEMA (default: 'app')
    - Managed by Alembic migrations
    """
    metadata = app_metadata
    schema = APP_SCHEMA


# ---------------------------------------------------------
# GIS BASE (Geographic/Spatial Models)
# ---------------------------------------------------------

class GISBase(DeclarativeBase):
    """
    Base ORM for geographic and spatial models.
    
    - All geographic entities (comunidades, provincias, municipios)
    - Spatial data with PostGIS types
    - Lives in GIS_SCHEMA (default: 'gis')
    - Managed by separate Alembic migrations
    """
    metadata = gis_metadata
    schema = GIS_SCHEMA


# ---------------------------------------------------------
# BACKWARD COMPATIBILITY
# ---------------------------------------------------------

# Alias for existing code - points to AppBase
Base = AppBase

# Export all bases
__all__ = ['AppBase', 'GISBase', 'Base', 'APP_SCHEMA', 'GIS_SCHEMA']
