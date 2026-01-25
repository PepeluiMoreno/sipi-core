#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inspeccionar datos de Aragón para entender su estructura
"""

import requests
import pandas as pd
from io import StringIO

URL_ESTRUCTURA = "https://opendata.aragon.es/ckan/datastore/dump/a9677651-72d9-49b4-8f90-c401d15896b3?format=csv&bom=True"

response = requests.get(URL_ESTRUCTURA, timeout=30)
response.raise_for_status()
df = pd.read_csv(StringIO(response.text), encoding='utf-8', sep=',')

print("Columnas del dataset:")
print(df.columns.tolist())
print("\nPrimeras 10 filas:")
print(df.head(10))
print("\nÚltimas 10 filas:")
print(df.tail(10))
