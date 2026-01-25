# models/__init__.py
from sipi.db.base import Base
from sipi.db.mixins import UUIDPKMixin, AuditMixin

# Actores
from .actores import (
    Privado, Administracion, AdministracionTitular, AgenciaInmobiliaria,
    ColegioProfesional, Diocesis, DiocesisTitular, Notaria, NotariaTitular,
    Tecnico, RegistroPropiedad, RegistroPropiedadTitular,
    EntidadReligiosa, EntidadReligiosaTitular
)

# Tipologías
from .tipologias import (
    TipoEstadoConservacion, TipoEstadoTratamiento, TipoRolTecnico,
    TipoCertificacionPropiedad, TipoTituloPropiedad, TipoDocumento, TipoInmueble, TipoMimeDocumento,
    TipoPersona, TipoTransmision, TipoVia, TipoEntidadReligiosa,
    TipoLicencia, FuenteDocumental, TipoUsoInmueble
)

# Geografía
from .geografia import ComunidadAutonoma, Provincia, Municipio

# Documentos
from .documentos import Documento, InmuebleDocumento

# Inmuebles (incluye InmuebleCita, InmuebleUso, InmuebleNivelProteccion)
from .inmuebles import (
    Inmueble, Inmatriculacion, InmuebleDenominacion,
    InmuebleOSMExt, InmuebleWDExt, InmuebleCita, InmuebleUso, InmuebleNivelProteccion
)

# Historiografía
from .historiografia import FuenteHistoriografica

# Figuras de Protección
from .figuras_proteccion import FiguraProteccion, NivelProteccion

# Transmisiones
from .transmisiones import Transmision, TransmisionAnunciante

# Intervenciones
from .intervenciones import Intervencion, IntervencionTecnico

# Subvenciones
from .subvenciones import IntervencionSubvencion, SubvencionAdministracion

# Usuarios
from .users import Usuario, Rol

# Discovery (Anuncios)
from .discovery import InmuebleRaw, DeteccionAnuncio

# OSM
from .osm import OSMPlace

# Historial (Sistema de Inteligencia) - DEPRECADO
# from .inmuebles import InmuebleEvento
# from .tipologias import EventoRegistrable

__all__ = [
    'Base', 'UUIDPKMixin', 'AuditMixin',
    # Actores
    'Privado', 'Administracion', 'AdministracionTitular', 'AgenciaInmobiliaria',
    'ColegioProfesional', 'Diocesis', 'DiocesisTitular', 'Notaria', 'NotariaTitular',
    'Tecnico', 'RegistroPropiedad', 'RegistroPropiedadTitular',
    'EntidadReligiosa', 'EntidadReligiosaTitular',
    # Tipologías
    'TipoEstadoConservacion', 'TipoEstadoTratamiento', 'TipoRolTecnico',
    'TipoCertificacionPropiedad', 'TipoTituloPropiedad', 'TipoDocumento', 'TipoInmueble', 'TipoMimeDocumento',
    'TipoPersona', 'TipoTransmision', 'TipoVia', 'TipoEntidadReligiosa',
    'TipoLicencia', 'FuenteDocumental', 'TipoUsoInmueble',
    # Geografía
    'ComunidadAutonoma', 'Provincia', 'Municipio',
    # Documentos
    'Documento', 'InmuebleDocumento',
    # Inmuebles
    'Inmueble', 'Inmatriculacion', 'InmuebleDenominacion',
    'InmuebleOSMExt', 'InmuebleWDExt', 'InmuebleCita', 'InmuebleUso', 'InmuebleNivelProteccion', 'InmuebleEvento',
    # Historiografía
    'FuenteHistoriografica',
    # Figuras de Protección
    'FiguraProteccion', 'NivelProteccion',
    # Transmisiones
    'Transmision', 'TransmisionAnunciante',
    # Intervenciones
    'Intervencion', 'IntervencionTecnico',
    # Subvenciones
    'IntervencionSubvencion', 'SubvencionAdministracion',
    # Usuarios
    'Usuario', 'Rol',
    # Discovery
    'InmuebleRaw', 'DeteccionAnuncio',
    # OSM
    'OSMPlace',
]