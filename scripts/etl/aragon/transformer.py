#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transformador de datos de Aragón.
"""

import pandas as pd
from typing import Dict, Any, List, Tuple
from uuid import uuid4
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from ..common.base import BaseTransformer


def mapear_tipo_organo_aragon(tipo: Any) -> str:
    """Mapea tipos de órgano de Aragón"""
    if pd.isna(tipo):
        return 'ORGANO'

    tipo_upper = str(tipo).upper()
    mapeo = {
        'CONSEJERÍA': 'CONSEJERIA',
        'DIRECCIÓN GENERAL': 'DIRECCION_GENERAL',
        'SECRETARÍA GENERAL': 'SECRETARIA_GENERAL',
        'VICESECRETARÍA': 'VICESECRETARIA',
        'SERVICIO': 'SERVICIO',
        'CENTRO': 'CENTRO',
        'AGENCIA': 'AGENCIA'
    }
    return mapeo.get(tipo_upper, 'ORGANO')


class AragonTransformer(BaseTransformer):
    """Transformador para datos de Aragón"""

    def __init__(self, comunidad_autonoma_id: str):
        self.comunidad_autonoma_id = comunidad_autonoma_id

    def _extraer_campo(self, row: pd.Series, nombres: List[str]) -> Any:
        """Extrae un campo probando varios nombres"""
        for nombre in nombres:
            valor = row.get(nombre)
            if not pd.isna(valor):
                return valor
        return None

    async def transform(self, raw_data: Tuple[pd.DataFrame, pd.DataFrame]) -> List[Dict[str, Any]]:
        """Transforma datos de Aragón"""
        print("🔄 Transformando datos de Aragón...")

        df_estructura, df_titulares = raw_data
        resultado = []
        administraciones_map = {}

        # Transformar estructura
        for idx, row in df_estructura.iterrows():
            nombre = self._extraer_campo(row, ['NOMBRE', 'nombre', 'nombre_organo', 'denominacion'])
            tipo = self._extraer_campo(row, ['TIPO', 'tipo', 'tipo_organo'])
            codigo = self._extraer_campo(row, ['CODIGO', 'codigo', 'codigo_organo'])

            if pd.isna(nombre):
                continue

            tipo_organo = mapear_tipo_organo_aragon(tipo)

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

            administraciones_map[codigo] = admin_data
            resultado.append({'tipo': 'administracion', 'data': admin_data})

        print(f"   Administraciones transformadas: {len(administraciones_map)}")

        # Transformar titulares
        titulares_count = 0
        for idx, row in df_titulares.iterrows():
            codigo_organo = self._extraer_campo(row, ['CODIGO_ORGANO', 'codigo_organo'])
            nombre_titular = self._extraer_campo(row, ['NOMBRE_TITULAR', 'nombre_titular', 'nombre'])
            cargo = self._extraer_campo(row, ['CARGO', 'cargo'])

            if pd.isna(codigo_organo) or pd.isna(nombre_titular) or codigo_organo not in administraciones_map:
                continue

            titular_data = {
                'id': str(uuid4()),
                'administracion_codigo': codigo_organo,
                'nombre': str(nombre_titular).strip(),
                'cargo': str(cargo).strip() if not pd.isna(cargo) else 'Titular',
                'fecha_inicio': datetime.utcnow()
            }

            resultado.append({'tipo': 'titular', 'data': titular_data})
            titulares_count += 1

        print(f"   Titulares transformados: {titulares_count}")
        return resultado
