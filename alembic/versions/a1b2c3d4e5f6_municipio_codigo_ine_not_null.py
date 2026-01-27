"""municipio_codigo_ine_not_null

Revision ID: a1b2c3d4e5f6
Revises: e8a4ac3a0dc4
Create Date: 2026-01-27

Hace obligatorio el campo codigo_ine en la tabla municipios.
IMPORTANTE: Antes de ejecutar esta migración, asegúrate de que todos los
municipios tienen codigo_ine poblado ejecutando el ETL de geografía.

Verificar con:
    SELECT COUNT(*) FROM sipi.municipios WHERE codigo_ine IS NULL OR codigo_ine = '';
    -- Debe retornar 0
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'e8a4ac3a0dc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMA = 'sipi'


def upgrade() -> None:
    # Verificar que no hay municipios sin codigo_ine antes de aplicar
    # Si hay registros sin codigo_ine, la migración fallará (lo cual es correcto)

    # Alterar columna codigo_ine a NOT NULL
    op.alter_column(
        'municipios',
        'codigo_ine',
        existing_type=sa.String(5),
        nullable=False,
        schema=SCHEMA
    )


def downgrade() -> None:
    # Revertir a nullable
    op.alter_column(
        'municipios',
        'codigo_ine',
        existing_type=sa.String(5),
        nullable=True,
        schema=SCHEMA
    )
