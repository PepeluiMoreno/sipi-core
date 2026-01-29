# db/metadata.py

import os
from sqlalchemy import MetaData
from db.registry import Base, APP_SCHEMA, GIS_SCHEMA

# Schemas que Alembic debe gestionar (desde variable de entorno)
# Ejemplo: DEFINED_SCHEMAS=app → solo gestiona app
# Ejemplo: DEFINED_SCHEMAS=app,gis → gestiona ambos
ALEMBIC_SCHEMAS = os.getenv("DEFINED_SCHEMAS", APP_SCHEMA).split(",")

# Metadata para tablas GIS (siempre existe, pero Alembic lo usa solo si está en ALEMBIC_SCHEMAS)
GISMetadata = MetaData(schema=GIS_SCHEMA)

def register_gis_table(table):
    """Registra una tabla en el schema GIS"""
    table.schema = GIS_SCHEMA
    table.to_metadata(GISMetadata)

def get_combined_metadata():
    """
    Construye metadata combinada SOLO con los schemas que Alembic debe gestionar.
    Esto permite tener tablas definidas en código pero no gestionadas por Alembic.
    """
    combined = MetaData()
    
    # Solo incluir APP si está en ALEMBIC_SCHEMAS
    if APP_SCHEMA in ALEMBIC_SCHEMAS:
        for table in Base.metadata.tables.values():
            if table.schema is None:
                table.schema = APP_SCHEMA
            table.to_metadata(combined)
    
    # Solo incluir GIS si está en ALEMBIC_SCHEMAS
    if GIS_SCHEMA in ALEMBIC_SCHEMAS:
        for table in GISMetadata.tables.values():
            table.to_metadata(combined)
    
    return combined

CombinedMetadata = get_combined_metadata()