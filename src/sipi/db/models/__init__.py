# models/__init__.py
"""
SIPI Database Models

This module provides a unified import interface for all database models,
organized by domain and schema:

- APP Schema: Business domain models (actors, properties, documents, etc.)
- GIS Schema: Geographic and spatial models (administrative divisions, OSM data)
"""

from sipi.db.base import Base, AppBase, GISBase
from sipi.db.mixins import UUIDPKMixin, AuditMixin

# ============================================================================
# ACTORS (APP Schema) - Organized by type
# ============================================================================

from .actores import (
    # Base classes
    PersonaMixin, TitularBase,
    
    # Notaries
    Notaria, NotariaTitular,
    
    # Property Registrars
    RegistroPropiedad, RegistroPropiedadTitular,
    
    # Public Administrations
    Administracion, AdministracionTitular,
    
    # Religious Entities
    Diocesis, DiocesisTitular,
    EntidadReligiosa, EntidadReligiosaTitular,
    
    # Technical Professionals
    Tecnico, ColegioProfesional,
    
    # Private Actors
    Privado, AgenciaInmobiliaria,
)

# ============================================================================
# GEOGRAPHY (GIS Schema)
# ============================================================================

from .geografia import (
    ComunidadAutonoma, 
    Provincia, 
    Municipio
)

# ============================================================================
# TYPOLOGIES (APP Schema)
# ============================================================================

from .tipologias import (
    TipoEstadoConservacion, TipoEstadoTratamiento, TipoRolTecnico,
    TipoCertificacionPropiedad, TipoTituloPropiedad, TipoDocumento, 
    TipoInmueble, TipoMimeDocumento, TipoPersona, TipoTransmision, 
    TipoVia, TipoEntidadReligiosa, TipoLicencia, FuenteDocumental, 
    TipoUsoInmueble
)

# ============================================================================
# DOCUMENTS (APP Schema)
# ============================================================================

from .documentos import (
    Documento, 
    InmuebleDocumento
)

# ============================================================================
# PROPERTIES (APP Schema)
# ============================================================================

from .inmuebles import (
    Inmueble, 
    Inmatriculacion, 
    InmuebleDenominacion,
    InmuebleOSMExt, 
    InmuebleWDExt, 
    InmuebleCita, 
    InmuebleUso, 
    InmuebleNivelProteccion
)

# ============================================================================
# HISTORIOGRAPHY (APP Schema)
# ============================================================================

from .historiografia import (
    FuenteHistoriografica
)

# ============================================================================
# PROTECTION FIGURES (APP Schema)
# ============================================================================

from .figuras_proteccion import (
    FiguraProteccion, 
    NivelProteccion
)

# ============================================================================
# TRANSMISSIONS (APP Schema)
# ============================================================================

from .transmisiones import (
    Transmision, 
    TransmisionAnunciante
)

# ============================================================================
# INTERVENTIONS (APP Schema)
# ============================================================================

from .intervenciones import (
    Intervencion, 
    IntervencionTecnico
)

# ============================================================================
# SUBSIDIES (APP Schema)
# ============================================================================

from .subvenciones import (
    IntervencionSubvencion, 
    SubvencionAdministracion
)

# ============================================================================
# USERS (APP Schema)
# ============================================================================

from .users import (
    Usuario, 
    Rol
)

# ============================================================================
# DISCOVERY (APP Schema)
# ============================================================================

from .discovery import (
    InmuebleRaw, 
    DeteccionAnuncio
)

# ============================================================================
# OSM (GIS Schema - could be moved to geografia package)
# ============================================================================

from .osm import (
    OSMPlace
)

# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    # Base classes
    'Base', 'AppBase', 'GISBase',
    'UUIDPKMixin', 'AuditMixin',
    
    # Actor base classes
    'PersonaMixin', 'TitularBase',
    
    # Notaries
    'Notaria', 'NotariaTitular',
    
    # Property Registrars
    'RegistroPropiedad', 'RegistroPropiedadTitular',
    
    # Public Administrations
    'Administracion', 'AdministracionTitular',
    
    # Religious Entities
    'Diocesis', 'DiocesisTitular',
    'EntidadReligiosa', 'EntidadReligiosaTitular',
    
    # Technical Professionals
    'Tecnico', 'ColegioProfesional',
    
    # Private Actors
    'Privado', 'AgenciaInmobiliaria',
    
    # Geography (GIS Schema)
    'ComunidadAutonoma', 'Provincia', 'Municipio',
    
    # Typologies
    'TipoEstadoConservacion', 'TipoEstadoTratamiento', 'TipoRolTecnico',
    'TipoCertificacionPropiedad', 'TipoTituloPropiedad', 'TipoDocumento', 
    'TipoInmueble', 'TipoMimeDocumento', 'TipoPersona', 'TipoTransmision', 
    'TipoVia', 'TipoEntidadReligiosa', 'TipoLicencia', 'FuenteDocumental', 
    'TipoUsoInmueble',
    
    # Documents
    'Documento', 'InmuebleDocumento',
    
    # Properties
    'Inmueble', 'Inmatriculacion', 'InmuebleDenominacion',
    'InmuebleOSMExt', 'InmuebleWDExt', 'InmuebleCita', 'InmuebleUso', 
    'InmuebleNivelProteccion',
    
    # Historiography
    'FuenteHistoriografica',
    
    # Protection Figures
    'FiguraProteccion', 'NivelProteccion',
    
    # Transmissions
    'Transmision', 'TransmisionAnunciante',
    
    # Interventions
    'Intervencion', 'IntervencionTecnico',
    
    # Subsidies
    'IntervencionSubvencion', 'SubvencionAdministracion',
    
    # Users
    'Usuario', 'Rol',
    
    # Discovery
    'InmuebleRaw', 'DeteccionAnuncio',
    
    # OSM
    'OSMPlace',
]
