#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ejecutar la migración de administraciones con jerarquía.

Ejecutar desde sipi-core:
    python scripts/run_migration_administraciones.py
"""

import asyncio
import sys
from pathlib import Path

# Agregar sipi-core al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sipi.db.sessions import async_session_maker
from sqlalchemy import text

async def run_migration():
    """Ejecuta la migración SQL"""
    print("=" * 80)
    print("🔄 EJECUTANDO MIGRACIÓN: Jerarquía de Administraciones")
    print("=" * 80)

    # Leer el archivo SQL
    migration_file = Path(__file__).parent / "migration_administraciones_jerarquia.sql"

    if not migration_file.exists():
        print(f"❌ Archivo de migración no encontrado: {migration_file}")
        return False

    print(f"📄 Leyendo archivo: {migration_file.name}")

    with open(migration_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Dividir en statements individuales
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip() and not stmt.strip().startswith('--')]

    print(f"📋 Se ejecutarán {len(statements)} statements")

    async with async_session_maker() as session:
        try:
            for idx, statement in enumerate(statements, 1):
                # Saltar comentarios y líneas vacías
                if statement.startswith('--') or not statement.strip():
                    continue

                print(f"\n[{idx}/{len(statements)}] Ejecutando statement...")

                # Mostrar primeras líneas del statement
                first_line = statement.split('\n')[0][:80]
                print(f"   {first_line}...")

                # Ejecutar el statement
                await session.execute(text(statement))
                print("   ✅ Completado")

            # Commit final
            await session.commit()
            print("\n" + "=" * 80)
            print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
            print("=" * 80)
            return True

        except Exception as e:
            await session.rollback()
            print(f"\n❌ ERROR durante la migración: {e}")
            print("   Se ha hecho rollback de todos los cambios")
            return False

if __name__ == "__main__":
    success = asyncio.run(run_migration())
    sys.exit(0 if success else 1)
