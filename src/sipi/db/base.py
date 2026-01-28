# app/db/base.py
import os
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

# ---------------------------------------------------------
# SCHEMA DE APLICACIÓN (ÚNICO QUE MIGRA ALEMBIC)
# ---------------------------------------------------------

APP_SCHEMA = (
    os.getenv("DATABASE_SCHEMA")
    or os.getenv("DB_SCHEMA")
    or "app"
)

# ---------------------------------------------------------
# METADATA DEL DOMINIO DE LA APP
# ---------------------------------------------------------

app_metadata = MetaData(schema=APP_SCHEMA)

# ---------------------------------------------------------
# BASE DECLARATIVA MODERNA (SQLAlchemy 2.x)
# ---------------------------------------------------------

class Base(DeclarativeBase):
    """
    Base ORM del dominio de aplicación.

    - Todas las tablas viven en APP_SCHEMA
    - Alembic SOLO debe apuntar aquí
    - GIS NO hereda de esta Base
    """
    metadata = app_metadata

    # Expuesto explícitamente (sin hacks)
    schema = APP_SCHEMA
