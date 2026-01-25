#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Loader compartido para administraciones.
"""

from typing import Dict, Any, List
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from sipi.db.sessions import async_session_maker
from sipi.db.models import Administracion, AdministracionTitular
from .base import BaseLoader


class AdministracionLoader(BaseLoader):
    """Cargador común para administraciones y titulares"""

    async def load(self, transformed_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """Carga administraciones y titulares en la base de datos"""
        stats = {
            'loaded': 0,
            'errors': 0,
            'administraciones': 0,
            'titulares': 0
        }

        async with async_session_maker() as session:
            codigo_to_id = {}

            # Fase 1: Cargar administraciones
            print("   Fase 1: Cargando administraciones...")
            for item in transformed_data:
                if item['tipo'] != 'administracion':
                    continue

                try:
                    data = item['data']
                    admin = Administracion(**data)
                    session.add(admin)

                    if data.get('codigo_oficial'):
                        codigo_to_id[data['codigo_oficial']] = data['id']

                    stats['administraciones'] += 1
                    stats['loaded'] += 1

                    if stats['administraciones'] % 100 == 0:
                        await session.flush()
                        print(f"      Procesadas {stats['administraciones']} administraciones...")

                except Exception as e:
                    stats['errors'] += 1
                    if stats['errors'] <= 5:
                        print(f"   ⚠️  Error cargando administración: {e}")

            await session.flush()
            print(f"   ✅ Administraciones cargadas: {stats['administraciones']}")

            # Fase 2: Cargar titulares
            print("   Fase 2: Cargando titulares...")
            for item in transformed_data:
                if item['tipo'] != 'titular':
                    continue

                try:
                    data = item['data'].copy()
                    codigo_organo = data.pop('administracion_codigo', None)

                    if not codigo_organo or codigo_organo not in codigo_to_id:
                        continue

                    data['administracion_id'] = codigo_to_id[codigo_organo]
                    titular = AdministracionTitular(**data)
                    session.add(titular)

                    stats['titulares'] += 1
                    stats['loaded'] += 1

                    if stats['titulares'] % 50 == 0:
                        await session.flush()
                        print(f"      Procesados {stats['titulares']} titulares...")

                except Exception as e:
                    stats['errors'] += 1
                    if stats['errors'] <= 5:
                        print(f"   ⚠️  Error cargando titular: {e}")

            await session.commit()
            print(f"   ✅ Titulares cargados: {stats['titulares']}")

        return stats
