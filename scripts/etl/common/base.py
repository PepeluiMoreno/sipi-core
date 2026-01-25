#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clases base para ETL de administraciones.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from pathlib import Path
import sys

# Agregar sipi-core al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from sipi.db.sessions import async_session_maker


class BaseExtractor(ABC):
    """Extractor base"""

    @abstractmethod
    async def extract(self) -> Any:
        """Extrae datos de la fuente"""
        pass


class BaseTransformer(ABC):
    """Transformador base"""

    @abstractmethod
    async def transform(self, raw_data: Any) -> List[Dict[str, Any]]:
        """Transforma datos crudos"""
        pass


class BaseLoader(ABC):
    """Cargador base"""

    @abstractmethod
    async def load(self, transformed_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """Carga datos en base de datos"""
        pass
