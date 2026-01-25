#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplica la migración manualmente usando SQL directo
"""

import asyncio
import sys
import os
from pathlib import Path

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sipi.db.sessions import async_session_maker
from sqlalchemy import text


async def main():
    """Aplicar migración manualmente"""
    async with async_session_maker() as session:
        print("Aplicando migración de administraciones...")

        # Agregar columnas a administraciones
        await session.execute(text("""
            ALTER TABLE sipi.administraciones
            ADD COLUMN IF NOT EXISTS codigo_oficial VARCHAR(100),
            ADD COLUMN IF NOT EXISTS administracion_padre_id VARCHAR(36),
            ADD COLUMN IF NOT EXISTS nivel_jerarquico VARCHAR(50),
            ADD COLUMN IF NOT EXISTS tipo_organo VARCHAR(100),
            ADD COLUMN IF NOT EXISTS orden_jerarquico INTEGER,
            ADD COLUMN IF NOT EXISTS valido_desde TIMESTAMP DEFAULT NOW(),
            ADD COLUMN IF NOT EXISTS valido_hasta TIMESTAMP,
            ADD COLUMN IF NOT EXISTS activa BOOLEAN DEFAULT TRUE NOT NULL;
        """))

        print("  ✅ Columnas agregadas a administraciones")

        # Crear índices
        await session.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_sipi_administraciones_codigo_oficial
            ON sipi.administraciones(codigo_oficial);
        """))
        await session.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_sipi_administraciones_administracion_padre_id
            ON sipi.administraciones(administracion_padre_id);
        """))
        await session.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_sipi_administraciones_nivel_jerarquico
            ON sipi.administraciones(nivel_jerarquico);
        """))
        await session.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_sipi_administraciones_tipo_organo
            ON sipi.administraciones(tipo_organo);
        """))
        await session.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_sipi_administraciones_orden_jerarquico
            ON sipi.administraciones(orden_jerarquico);
        """))
        await session.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_sipi_administraciones_valido_desde
            ON sipi.administraciones(valido_desde);
        """))
        await session.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_sipi_administraciones_valido_hasta
            ON sipi.administraciones(valido_hasta);
        """))
        await session.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_sipi_administraciones_activa
            ON sipi.administraciones(activa);
        """))

        print("  ✅ Índices creados")

        # Agregar foreign key
        try:
            await session.execute(text("""
                ALTER TABLE sipi.administraciones
                ADD CONSTRAINT fk_administracion_padre
                FOREIGN KEY (administracion_padre_id)
                REFERENCES sipi.administraciones(id)
                ON DELETE SET NULL;
            """))
            print("  ✅ Foreign key agregado")
        except Exception as e:
            print(f"  ⚠️  Foreign key ya existe o error: {e}")

        await session.commit()

        print("\n✅ Migración aplicada exitosamente")


if __name__ == "__main__":
    asyncio.run(main())
