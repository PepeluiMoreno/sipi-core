#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar el esquema de la tabla administraciones
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sipi.db.sessions import async_session_maker
from sqlalchemy import text


async def main():
    """Verificar columnas de administraciones"""
    async with async_session_maker() as session:
        # Verificar columnas de la tabla administraciones
        result = await session.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'sipi'
            AND table_name = 'administraciones'
            ORDER BY ordinal_position;
        """))

        print("=" * 80)
        print("COLUMNAS EN sipi.administraciones:")
        print("=" * 80)

        for row in result:
            print(f"  {row[0]:40} {row[1]:20} nullable={row[2]}")


if __name__ == "__main__":
    asyncio.run(main())
