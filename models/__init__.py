
# models/__init__.py
"""
SIPI Database Models

This module provides a unified import interface for all database models,
organized by domain and schema:

- APP Schema: Business domain models (actors, properties, documents, etc.)
- GIS Schema: Geographic and spatial models (administrative divisions, OSM data)
"""

# ============================================================================
# BASE CLASSES (Primero siempre)
# ============================================================================
from db.registry import Base
from mixins import UUIDPKMixin, AuditMixin

# ============================================================================
# USERS (DEBE IR PRIMERO - AuditMixin y muchos otros dependen de esto)
# ============================================================================
from models.users import Usuario, Rol

# ============================================================================
# TYPOLOGIES (APP Schema - Sin dependencias de actores)
# ============================================================================
from models.tipologias import (
    TipoEstadoConservacion, TipoEstadoTratamiento, TipoRolTecnico,
    TipoCertificacionPropiedad, TipoTituloPropiedad, TipoDocumento, 
    TipoInmueble, TipoMimeDocumento, TipoPersona, TipoTransmision, 
    TipoVia, TipoEntidadReligiosa, TipoLicencia, FuenteDocumental, 
    TipoUsoInmueble
)

# ============================================================================
# GEOGRAPHY (APP Schema - Sin dependencias de actores)
# ============================================================================
from models.geografia import (
    ComunidadAutonoma, 
    Provincia, 
    Municipio
)

# ============================================================================
# ACTORS BASE (Clases base abstractas sin dependencias)
# ============================================================================
from models.actores_base import PersonaMixin, TitularBase

# ============================================================================
# ACTORS (APP Schema) - Ordenados por dependencias de Foreign Keys
# ============================================================================

# 1. Notarios (no tienen FK a otros actores)
from models.notarios import Notaria, NotariaTitular  

# 2. Registradores (no tienen FK a otros actores)
from models.registradores import RegistroPropiedad, RegistroPropiedadTitular

# 3. Administraciones (tienen updated_by_id -> usuarios.id, ya importado arriba)
from models.administraciones import Administracion, AdministracionTitular

# 4. Entidades Religiosas (Diocesis antes que EntidadReligiosa por FKs)
from models.entidades_religiosas import Diocesis, DiocesisTitular
from models.entidades_religiosas import EntidadReligiosa, EntidadReligiosaTitular

# 5. Técnicos (pueden tener FK a tipologías y usuarios)
from models.tecnicos import Tecnico, ColegioProfesional

# 6. Privados y Agencias (sin dependencias críticas)
from models.privados import Privado
from models.agencias import AgenciaInmobiliaria

# ============================================================================
# DOCUMENTS (APP Schema - Depende de actores)
# ============================================================================
from models.documentos import (
    Documento, 
    InmuebleDocumento
)

# ============================================================================
# PROPERTIES (APP Schema - Depende de documentos, geografía y actores)
# ============================================================================
from models.inmuebles import (
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
from models.historiografia import (
    FuenteHistoriografica
)

# ============================================================================
# PROTECTION FIGURES (APP Schema)
# ============================================================================
from models.figuras_proteccion import (
    FiguraProteccion, 
    NivelProteccion
)

# ============================================================================
# TRANSMISSIONS (APP Schema - Depende de inmuebles y actores)
# ============================================================================
from models.transmisiones import (
    Transmision, 
    TransmisionAnunciante
)

# ============================================================================
# INTERVENTIONS (APP Schema - Depende de inmuebles y técnicos)
# ============================================================================
from models.intervenciones import (
    Intervencion, 
    IntervencionTecnico
)

# ============================================================================
# SUBSIDIES (APP Schema - Depende de intervenciones y administraciones)
# ============================================================================
from models.subvenciones import (
    IntervencionSubvencion, 
    SubvencionAdministracion
)

# ============================================================================
# DISCOVERY (APP Schema)
# ============================================================================
from models.discovery import (
    InmuebleRaw, 
    DeteccionAnuncio
)

# ============================================================================
# OSM (GIS Schema - could be moved to geografia package)
# ============================================================================
from models.osm import (
    OSMPlace
)

# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    # Base classes
    'Base',
    'UUIDPKMixin', 'AuditMixin',

    # User
    'Usuario', 'Rol',

    # Typologies
    'TipoEstadoConservacion', 'TipoEstadoTratamiento', 'TipoRolTecnico',
    'TipoCertificacionPropiedad', 'TipoTituloPropiedad', 'TipoDocumento', 
    'TipoInmueble', 'TipoMimeDocumento', 'TipoPersona', 'TipoTransmision', 
    'TipoVia', 'TipoEntidadReligiosa', 'TipoLicencia', 'FuenteDocumental', 
    'TipoUsoInmueble',

    # Geography (GIS Schema)
    'ComunidadAutonoma', 'Provincia', 'Municipio',

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
    
    # Discovery
    'InmuebleRaw', 'DeteccionAnuncio',
    
    # OSM
    'OSMPlace',
]