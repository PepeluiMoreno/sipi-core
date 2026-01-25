#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extractor de datos de Asturias.
"""

import requests
import pandas as pd
from io import StringIO
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from ..common.base import BaseExtractor


class AsturiasExtractor(BaseExtractor):
    """Extractor para datos de Asturias"""

    URL_BASE = "https://datos.gob.es/es/catalogo/a03002951-estructuras-organicas"

    async def extract(self) -> pd.DataFrame:
        """Descarga datos de Asturias"""
        print("📥 Descargando datos de Asturias...")

        try:
            from bs4 import BeautifulSoup

            response = requests.get(self.URL_BASE, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            download_links = soup.find_all('a', href=lambda href: href and ('csv' in href.lower() or 'json' in href.lower()))

            dataset_url = None
            for link in download_links:
                href = link.get('href')
                if 'asturias' in href.lower() or 'astur' in href.lower():
                    dataset_url = href if href.startswith('http') else f"https://datos.gob.es{href}"
                    break

            if not dataset_url:
                print("   No se encontró URL específica, intentando URL genérica...")
                dataset_url = "https://datos.gob.es/es/catalogo/a03002951-estructuras-organicas.csv"

            print(f"   URL encontrada: {dataset_url}")

            response = requests.get(dataset_url, timeout=30)
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

        except Exception as e:
            print(f"❌ Error en extracción: {e}")
            raise
