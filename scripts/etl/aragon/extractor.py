#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extractor de datos de Aragón.
Utiliza datos abiertos del Gobierno de Aragón.
"""

import requests
import pandas as pd
from io import StringIO
from typing import Tuple
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from ..common.base import BaseExtractor


class AragonExtractor(BaseExtractor):
    """Extractor para datos de Aragón"""

    # URLs de datos abiertos de Aragón
    URL_ESTRUCTURA = "https://opendata.aragon.es/ckan/datastore/dump/a9677651-72d9-49b4-8f90-c401d15896b3?format=csv&bom=True"
    URL_TITULARES = "https://opendata.aragon.es/ckan/datastore/dump/10107649-60f0-4519-906c-e2df6dfcd4de?format=csv&bom=True"

    async def extract(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Descarga estructura y titulares de Aragón"""
        print("📥 Descargando datos de Aragón...")

        print("   Descargando estructura...")
        response_est = requests.get(self.URL_ESTRUCTURA, timeout=30)
        response_est.raise_for_status()
        df_estructura = pd.read_csv(StringIO(response_est.text), encoding='utf-8', sep=',')
        print(f"   ✅ Estructura: {len(df_estructura)} registros")

        print("   Descargando titulares...")
        response_tit = requests.get(self.URL_TITULARES, timeout=30)
        response_tit.raise_for_status()
        df_titulares = pd.read_csv(StringIO(response_tit.text), encoding='utf-8', sep=',')
        print(f"   ✅ Titulares: {len(df_titulares)} registros")

        return df_estructura, df_titulares
