# models/ Tipologias.py
from __future__ import annotations
from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Boolean, Integer, ForeignKey
from sipi.db.base import Base
from sipi.db.mixins import UUIDPKMixin, AuditMixin

if TYPE_CHECKING:
    from .inmuebles import InmuebleEvento


class  TipologiaBase(UUIDPKMixin, AuditMixin, Base):
    __abstract__ = True
    nombre: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)

class TipoEstadoConservacion( TipologiaBase):
    __tablename__ = "estados_conservacion"
    inmuebles: Mapped[list["Inmueble"]] = relationship("Inmueble", back_populates="estado_conservacion")

class TipoEstadoTratamiento( TipologiaBase):
    __tablename__ = "estados_tratamiento"
    inmuebles: Mapped[list["Inmueble"]] = relationship("Inmueble", back_populates="estado_tratamiento")

class TipoRolTecnico( TipologiaBase):
    __tablename__ = "roles_tecnico"
    tecnicos: Mapped[list["Tecnico"]] = relationship("Tecnico", back_populates="rol_tecnico")

class TipoCertificacionPropiedad( TipologiaBase):
    __tablename__ = "tipos_certificacion_propiedad"
    transmisiones: Mapped[list["Transmision"]] = relationship("Transmision", back_populates="tipo_certificacion_propiedad")
    inmatriculaciones: Mapped[list["Inmatriculacion"]] = relationship("Inmatriculacion", back_populates="tipo_certificacion_propiedad")

class TipoTituloPropiedad(UUIDPKMixin, AuditMixin, Base):
    """
    Catálogo de tipos de títulos de propiedad.
    Se usa en el proceso de INMATRICULACION para especificar el tipo de título presentado.
    """
    __tablename__ = "tipos_titulo_propiedad"

    codigo: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(200))
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

class TipoDocumento( TipologiaBase):
    __tablename__ = "tipos_documento"
    documentos: Mapped[list["Documento"]] = relationship("Documento", back_populates="tipo_documento")

class TipoInmueble( TipologiaBase):
    __tablename__ = "tipos_inmueble"
    inmuebles: Mapped[list["Inmueble"]] = relationship("Inmueble", back_populates="tipo_inmueble")

class TipoMimeDocumento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_mime_documento"
    tipo_mime: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    extension: Mapped[str] = mapped_column(String(10))
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)

class TipoPersona( TipologiaBase):
    __tablename__ = "tipos_persona"

class TipoTransmision( TipologiaBase):
    __tablename__ = "tipos_transmision"
    transmisiones: Mapped[list["Transmision"]] = relationship("Transmision", back_populates="tipo_transmision")

class TipoVia( TipologiaBase):
    __tablename__ = "tipos_via"

class TipoEntidadReligiosa(TipologiaBase):
    """Tipos de entidades religiosas: Orden, Congregación, Instituto de Vida Consagrada, etc."""
    __tablename__ = "tipos_entidad_religiosa"
    entidades_religiosas: Mapped[list["EntidadReligiosa"]] = relationship("EntidadReligiosa", back_populates="tipo_entidad")


class TipoLicencia(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_licencia"
    codigo: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    nombre_corto: Mapped[str | None] = mapped_column(String(100), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    url_licencia: Mapped[str | None] = mapped_column(String(500), nullable=True)
    url_legal: Mapped[str | None] = mapped_column(String(500), nullable=True)
    requiere_atribucion: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    permite_uso_comercial: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    permite_derivadas: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    requiere_compartir_igual: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    es_libre: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    es_open_source: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    es_copyleft: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    version: Mapped[str | None] = mapped_column(String(20), nullable=True)
    jurisdiccion: Mapped[str | None] = mapped_column(String(50), nullable=True)
    familia: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    icono_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    color_hex: Mapped[str | None] = mapped_column(String(7), nullable=True)
    popularidad: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    recomendada: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    obsoleta: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    documentos: Mapped[list["Documento"]] = relationship("Documento", back_populates="tipo_licencia")
    fuentes_documentales: Mapped[list["FuenteDocumental"]] = relationship("FuenteDocumental", back_populates="licencia_predeterminada", foreign_keys="[FuenteDocumental.licencia_predeterminada_id]")
    
    @property
    def badge_text(self) -> str:
        return self.nombre_corto or self.codigo
    
    @property
    def es_creative_commons(self) -> bool:
        return self.familia == "Creative Commons"


class TipoUsoInmueble(TipologiaBase):
    """
    Catálogo de tipos de uso de inmuebles.

    Define los diferentes usos que puede tener un inmueble a lo largo de su historia.
    Ejemplos: Religioso, Cultural, Turístico, Residencial, No declarado
    """
    __tablename__ = "tipos_uso_inmueble"

    codigo: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)

    # Relación inversa
    usos_inmuebles: Mapped[List["InmuebleUso"]] = relationship("InmuebleUso", back_populates="tipo_uso")


# ============================================================================
# DEPRECADO: EventoRegistrable
# ============================================================================
# Los eventos ahora se representan mediante tablas específicas:
# - Inmatriculación → tabla inmatriculaciones
# - Enajenación → tabla transmisiones
# - Intervención arquitectónica → tabla intervenciones
# - Cambio de uso → tabla inmuebles_usos
#
# class EventoRegistrable(TipologiaBase):
#     """
#     DEPRECADO: Catálogo de tipos de eventos registrables.
#     Usar tablas específicas para cada tipo de evento.
#     """
#     __tablename__ = "eventos_registrables"
#
#     codigo: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
#     categoria: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
#     activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
#
#     eventos: Mapped[List["InmuebleEvento"]] = relationship("InmuebleEvento", back_populates="tipo_evento")


class FuenteDocumental(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "fuentes_documentales"
    codigo: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    url_fuente: Mapped[str | None] = mapped_column(String(500), nullable=True)
    es_externa: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    requiere_url_externa: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    permite_metadata_extra: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    licencia_predeterminada_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("tipos_licencia.id"), nullable=True)
    categoria: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    soporta_sincronizacion: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    frecuencia_sync_dias: Mapped[int | None] = mapped_column(Integer, nullable=True)
    api_endpoint: Mapped[str | None] = mapped_column(String(500), nullable=True)
    requiere_autenticacion: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    icono: Mapped[str | None] = mapped_column(String(100), nullable=True)
    color_hex: Mapped[str | None] = mapped_column(String(7), nullable=True)
    orden: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    activa: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    licencia_predeterminada: Mapped["TipoLicencia"] = relationship("TipoLicencia", foreign_keys=[licencia_predeterminada_id], back_populates="fuentes_documentales")
    documentos: Mapped[list["Documento"]] = relationship("Documento", back_populates="fuente_documental")

    @property
    def badge_text(self) -> str:
        return self.nombre

    @property
    def necesita_storage_propio(self) -> bool:
        return not self.requiere_url_externa