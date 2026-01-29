# db/metadata.py
"""
Centraliza metadatas y schemas para todo el proyecto.
Compatible con Alembic, multi-schema y Base del registry.

Uso:

1. Para modelos APP, seguir usando Base del registry normalmente.
2. Para modelos GIS, definir la tabla y luego registrar con `register_gis_table`.

Ejemplo de modelo GIS (comentado):

    from sqlalchemy import Column, Integer, String
    from db.metadata import GISMetadata, register_gis_table
    from db.registry import Base

    class MunicipioGIS(Base):
        __tablename__ = "municipios_gis"
        id = Column(Integer, primary_key=True)
        nombre = Column(String(255), nullable=False)

    # Registrar tabla en metadata GIS para Alembic
    register_gis_table(MunicipioGIS.__table__)
"""

from sqlalchemy import MetaData
from db.registry import Base

# ----------------------------
# SCHEMAS
# ----------------------------
APP_SCHEMA = "app"      # Esquema principal (territorios, actores, etc.)
GIS_SCHEMA = "gis"      # Esquema geográfico (placeholder)

# ----------------------------
# METADATA POR ESQUEMA
# ----------------------------
AppMetadata = Base.metadata           # Todas las tablas actuales (APP)
GISMetadata = MetaData(schema=GIS_SCHEMA)  # Metadata para futuras tablas GIS

# ----------------------------
# REGISTRO DINÁMICO DE TABLAS GIS
# ----------------------------
def register_gis_table(table):
    """
    Asigna una tabla nueva al schema GIS y la agrega al CombinedMetadata.
    Uso: llamar en cada modelo GIS al final de la definición.
    """
    table.schema = GIS_SCHEMA
    table.to_metadata(GISMetadata)

# ----------------------------
# METADATA COMBINADA PARA ALEMBIC
# ----------------------------
CombinedMetadata = MetaData()
for table in AppMetadata.tables.values():
    table.to_metadata(CombinedMetadata)
for table in GISMetadata.tables.values():
    table.to_metadata(CombinedMetadata)

