# models/geografia/__init__.py
"""
Geographic Models Package (GIS Schema)

This package contains all geographic and spatial models that live
in the GIS schema, separate from business logic models.
"""

from .divisiones import ComunidadAutonoma, Provincia, Municipio

__all__ = [
    'ComunidadAutonoma',
    'Provincia',
    'Municipio',
]
