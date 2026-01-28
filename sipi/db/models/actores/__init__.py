# models/actores/__init__.py
"""
Actors Package

This package contains all actor models organized by type:
- Notaries and notarial offices
- Property registrars and registries
- Public administrations
- Religious entities (dioceses, orders, congregations)
- Technical professionals
- Private individuals and commercial entities

All models use the APP schema for business logic.
"""

from ._base import PersonaMixin, TitularBase

from .notarios import (
    Notaria,
    NotariaTitular,
)

from .registradores import (
    RegistroPropiedad,
    RegistroPropiedadTitular,
)

from .administraciones import (
    Administracion,
    AdministracionTitular,
)

from .entidades_religiosas import (
    Diocesis,
    DiocesisTitular,
    EntidadReligiosa,
    EntidadReligiosaTitular,
)

from .tecnicos import (
    Tecnico,
    ColegioProfesional,
)

from .privados import (
    Privado,
    AgenciaInmobiliaria,
)

__all__ = [
    # Base classes
    'PersonaMixin',
    'TitularBase',
    
    # Notaries
    'Notaria',
    'NotariaTitular',
    
    # Property Registrars
    'RegistroPropiedad',
    'RegistroPropiedadTitular',
    
    # Public Administrations
    'Administracion',
    'AdministracionTitular',
    
    # Religious Entities
    'Diocesis',
    'DiocesisTitular',
    'EntidadReligiosa',
    'EntidadReligiosaTitular',
    
    # Technical Professionals
    'Tecnico',
    'ColegioProfesional',
    
    # Private Actors
    'Privado',
    'AgenciaInmobiliaria',
]
