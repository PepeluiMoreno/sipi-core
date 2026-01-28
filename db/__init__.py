# models/__init__.py
"""
SIPI Database Models

This module provides a unified import interface for all database models,
organized by domain and schema:

- APP Schema: Business domain models (actors, properties, documents, etc.)
- GIS Schema: Geographic and spatial models (administrative divisions, OSM data)
"""

from .models.base import Base, AppBase, GISBase
from .mixins import UUIDPKMixin, AuditMixin

# ============================================================================
# ACTORS (APP Schema) - Organized by type
# ============================================================================

from db.models import (
    # Base classes
    PersonaMixin, TitularBase,
 
    # Notaries    Notaria, NotariaTitular,
    
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

from .models.geografia import (
    ComunidadAutonoma, 
    Provincia, 
    Municipio
)

# ============================================================================
# TYPOLOGIES (APP Schema)
# ============================================================================

from .models.tipologias import (
    TipoEstadoConservacion, TipoEstadoTratamiento, TipoRolTecnico,
    TipoCertificacionPropiedad, TipoTituloPropiedad, TipoDocumento, 
    TipoInmueble, TipoMimeDocumento, TipoPersona, TipoTransmision, 
    TipoVia, TipoEntidadReligiosa, TipoLicencia, FuenteDocumental, 
    TipoUsoInmueble
)

# ============================================================================
# DOCUMENTS (APP Schema)
# ============================================================================

from .models.documentos import (
    Documento, 
    InmuebleDocumento
)

# ============================================================================
# PROPERTIES (APP Schema)
# ============================================================================

from .models.inmuebles import (
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

from .models.historiografia import (
    FuenteHistoriografica
)

# ============================================================================
# PROTECTION FIGURES (APP Schema)
# ============================================================================

from .models.figuras_proteccion import (
    FiguraProteccion, 
    NivelProteccion
)

# ============================================================================
# TRANSMISSIONS (APP Schema)
# ============================================================================

from .models.transmisiones import (
    Transmision, 
    TransmisionAnunciante
)

# ============================================================================
# INTERVENTIONS (APP Schema)
# ============================================================================

from .models.intervenciones import (
    Intervencion, 
    IntervencionTecnico
)

# ============================================================================
# SUBSIDIES (APP Schema)
# ============================================================================

from .models.subvenciones import (
    IntervencionSubvencion, 
    SubvencionAdministracion
)

# ============================================================================
# USERS (APP Schema)
# ============================================================================

from .models.users import (
    Usuario, 
    Rol
)

# ============================================================================
# DISCOVERY (APP Schema)
# ============================================================================

from .models.discovery import (
    InmuebleRaw, 
    DeteccionAnuncio
)

# ============================================================================
# OSM (GIS Schema - could be moved to geografia package)
# ============================================================================

from .models.osm import (
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
