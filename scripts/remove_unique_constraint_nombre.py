#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Eliminar constraint UNIQUE de la columna nombre en administraciones
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
    """Eliminar constraint UNIQUE"""
    async with async_session_maker() as session:
        print("Eliminando constraint UNIQUE de nombre...")

        try:
            await session.execute(text("""
                ALTER TABLE sipi.administraciones
                DROP CONSTRAINT IF EXISTS ix_sipi_administraciones_nombre;
            """))
            print("  ✅ Constraint eliminado")
        except Exception as e:
            print(f"  ⚠️  Error o constraint no existe: {e}")

        await session.commit()

        print("\n✅ Completado")


if __name__ == "__main__":
    asyncio.run(main())
