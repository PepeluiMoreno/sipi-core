#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extractor de datos de Andalucía.
"""

import requests
import pandas as pd
from io import StringIO
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from ..common.base import BaseExtractor


class AndaluciaExtractor(BaseExtractor):
    """Extractor para datos de Andalucía"""

    URL_ESTRUCTURA = "https://datos.juntadeandalucia.es/api/v0/basic-data/all?format=csv"

    async def extract(self) -> pd.DataFrame:
        """Descarga datos de Andalucía"""
        print("📥 Descargando datos de Andalucía...")

        response = requests.get(self.URL_ESTRUCTURA, timeout=30)
        response.raise_for_status()

        # Intentar diferentes formatos
        for enc in ['utf-8', 'latin-1']:
            for sep in [';', ',']:
                try:
                    df = pd.read_csv(StringIO(response.text), encoding=enc, sep=sep)
                    if len(df.columns) > 1:
                        print(f"   Formato detectado: encoding={enc}, sep='{sep}'")
                        print(f"   ✅ Datos obtenidos: {len(df)} registros")
                        return df
                except:
                    continue

        raise ValueError("No se pudo parsear el CSV")
