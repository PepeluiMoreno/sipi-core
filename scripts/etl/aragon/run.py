#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script ETL para Aragón.
Ejecutar desde sipi-core: python scripts/etl/aragon/run.py
"""

import asyncio
import sys
import os
from pathlib import Path

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Agregar sipi-core al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from sqlalchemy import select
from sipi.db.sessions import async_session_maker
from sipi.db.models import ComunidadAutonoma

from .extractor import AragonExtractor
from .transformer import AragonTransformer
from ..common.loaders import AdministracionLoader


async def main():
    """Función principal"""
    print("=" * 80)
    print("🇪🇸 ETL ADMINISTRACIONES - ARAGÓN")
    print("=" * 80)

    # Verificar comunidad autónoma
    async with async_session_maker() as session:
        result = await session.execute(
            select(ComunidadAutonoma).where(ComunidadAutonoma.nombre == "Aragón")
        )
        aragon = result.scalar_one_or_none()

        if not aragon:
            print("❌ Comunidad Autónoma de Aragón no encontrada")
            print("   Ejecuta primero el seeding geográfico")
            return

        print(f"✅ Comunidad Autónoma: {aragon.nombre} (ID: {aragon.id})")

    try:
        # Extract
        extractor = AragonExtractor()
        raw_data = await extractor.extract()

        # Transform
        transformer = AragonTransformer(comunidad_autonoma_id=aragon.id)
        transformed_data = await transformer.transform(raw_data)

        # Load
        loader = AdministracionLoader()
        print("💾 Cargando datos en base de datos...")
        stats = await loader.load(transformed_data)

        print("\n" + "=" * 80)
        print("✅ ETL COMPLETADO")
        print(f"   - Administraciones: {stats['administraciones']}")
        print(f"   - Titulares: {stats['titulares']}")
        print(f"   - Total: {stats['loaded']} registros")
        if stats['errors'] > 0:
            print(f"   - Errores: {stats['errors']}")
        print("=" * 80)

    except Exception as e:
        print("\n" + "=" * 80)
        print(f"❌ ERROR: {e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
