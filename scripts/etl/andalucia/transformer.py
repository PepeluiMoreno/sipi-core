#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transformador de datos de Andalucía.
"""

import pandas as pd
from typing import Dict, Any, List
from uuid import uuid4
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from ..common.base import BaseTransformer


def mapear_tipo_organo_andalucia(tipo: Any) -> str:
    """Mapea tipos de órgano de Andalucía"""
    if pd.isna(tipo):
        return 'ORGANO'

    tipo_upper = str(tipo).upper()
    mapeo = {
        'CONSEJERÍA': 'CONSEJERIA',
        'CONSEJERIA': 'CONSEJERIA',
        'DIRECCIÓN GENERAL': 'DIRECCION_GENERAL',
        'DIRECCION GENERAL': 'DIRECCION_GENERAL',
        'SECRETARÍA GENERAL': 'SECRETARIA_GENERAL',
        'SECRETARIA GENERAL': 'SECRETARIA_GENERAL',
        'AGENCIA': 'AGENCIA',
        'SERVICIO': 'SERVICIO',
        'CENTRO': 'CENTRO',
        'DELEGACIÓN': 'DELEGACION'
    }
    return mapeo.get(tipo_upper, 'ORGANO')


class AndaluciaTransformer(BaseTransformer):
    """Transformador para datos de Andalucía"""

    def __init__(self, comunidad_autonoma_id: str):
        self.comunidad_autonoma_id = comunidad_autonoma_id

    def _extraer_campo(self, row: pd.Series, nombres: List[str]) -> Any:
        """Extrae un campo probando varios nombres"""
        for nombre in nombres:
            valor = row.get(nombre)
            if not pd.isna(valor):
                return valor
        return None

    async def transform(self, raw_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Transforma datos de Andalucía"""
        print("🔄 Transformando datos de Andalucía...")

        resultado = []
        errores = 0

        for idx, row in raw_data.iterrows():
            try:
                nombre = self._extraer_campo(row, ['nombre', 'denominacion', 'titulo'])
                tipo = self._extraer_campo(row, ['tipo_organo', 'tipo'])
                codigo = self._extraer_campo(row, ['codigo', 'id'])

                if pd.isna(nombre) or not str(nombre).strip():
                    continue

                tipo_organo = mapear_tipo_organo_andalucia(tipo)

                admin_data = {
                    'id': str(uuid4()),
                    'nombre': str(nombre).strip(),
                    'ambito': tipo_organo,
                    'nivel_jerarquico': 'AUTONOMICO',
                    'tipo_organo': tipo_organo,
                    'codigo_oficial': str(codigo).strip() if codigo and not pd.isna(codigo) else None,
                    'comunidad_autonoma_id': self.comunidad_autonoma_id,
                    'activa': True,
                    'valido_desde': datetime.utcnow()
                }

                resultado.append({'tipo': 'administracion', 'data': admin_data})

            except Exception as e:
                errores += 1
                if errores <= 5:
                    print(f"   ⚠️  Error transformando fila {idx}: {e}")

        print(f"   Administraciones transformadas: {len(resultado)}")
        if errores > 0:
            print(f"   Errores: {errores}")

        return resultado
