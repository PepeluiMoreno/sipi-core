# models/geografia/divisiones.py
"""
Geographic Administrative Divisions (GIS Schema)

This module contains the geographic entities that form the administrative
structure of Spain. These models use the GIS schema for better separation
of spatial data from business logic.
"""

from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Index

from sipi.db.base import GISBase
from sipi.db.mixins import UUIDPKMixin, AuditMixin


class ComunidadAutonoma(UUIDPKMixin, AuditMixin, GISBase):
    """
    Autonomous Community of Spain (Comunidad Autónoma)
    
    Top-level administrative division in Spain.
    Lives in GIS schema as it's primarily geographic reference data.
    """
    __tablename__ = "comunidades_autonomas"

    codigo_ine: Mapped[str] = mapped_column(
        String(2), 
        unique=True, 
        index=True, 
        nullable=False,
        comment="INE official code (2 digits)"
    )
    nombre_oficial: Mapped[str] = mapped_column(
        String(100), 
        index=True, 
        nullable=False,
        comment="Official name in Spanish"
    )
    nombre_cooficial: Mapped[Optional[str]] = mapped_column(
        String(100),
        comment="Co-official name in regional language"
    )
    nombre_alternativo: Mapped[Optional[str]] = mapped_column(
        String(100),
        comment="Alternative or historical name"
    )

    # Relationships
    # Note: These relationships point to models in the APP schema
    # Cross-schema relationships are supported in PostgreSQL
    provincias: Mapped[list["Provincia"]] = relationship(
        "Provincia", 
        back_populates="comunidad_autonoma", 
        cascade="all, delete-orphan"
    )
    
    # Cross-schema relationships to APP schema
    inmuebles: Mapped[list["Inmueble"]] = relationship(
        "Inmueble", 
        back_populates="comunidad_autonoma"
    )
    figuras_proteccion: Mapped[list["FiguraProteccion"]] = relationship(
        "FiguraProteccion", 
        back_populates="comunidad_autonoma"
    )
    administraciones: Mapped[list["Administracion"]] = relationship(
        "Administracion", 
        back_populates="comunidad_autonoma"
    )

    __table_args__ = (
        Index('ix_gis_ccaa_codigo_ine', 'codigo_ine'),
        Index('ix_gis_ccaa_nombre', 'nombre_oficial'),
    )

    def __repr__(self) -> str:
        return f"<ComunidadAutonoma {self.codigo_ine} - {self.nombre_oficial}>"


class Provincia(UUIDPKMixin, AuditMixin, GISBase):
    """
    Province of Spain (Provincia)
    
    Second-level administrative division.
    Lives in GIS schema as geographic reference data.
    """
    __tablename__ = "provincias"

    codigo_ine: Mapped[str] = mapped_column(
        String(2), 
        unique=True, 
        index=True, 
        nullable=False,
        comment="INE official code (2 digits)"
    )
    nombre_oficial: Mapped[str] = mapped_column(
        String(100), 
        index=True, 
        nullable=False,
        comment="Official name"
    )
    nombre_cooficial: Mapped[Optional[str]] = mapped_column(
        String(100),
        comment="Co-official name in regional language"
    )
    nombre_alternativo: Mapped[Optional[str]] = mapped_column(
        String(100),
        comment="Alternative or historical name"
    )
    
    # Foreign key to parent geographic entity (same schema)
    comunidad_autonoma_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("gis.comunidades_autonomas.id"), 
        index=True, 
        nullable=False
    )

    # Relationships
    comunidad_autonoma: Mapped["ComunidadAutonoma"] = relationship(
        "ComunidadAutonoma", 
        back_populates="provincias"
    )
    municipios: Mapped[list["Municipio"]] = relationship(
        "Municipio", 
        back_populates="provincia", 
        cascade="all, delete-orphan"
    )
    
    # Cross-schema relationships to APP schema
    inmuebles: Mapped[list["Inmueble"]] = relationship(
        "Inmueble", 
        back_populates="provincia"
    )
    administraciones: Mapped[list["Administracion"]] = relationship(
        "Administracion", 
        back_populates="provincia"
    )

    __table_args__ = (
        Index('ix_gis_provincia_codigo_ine', 'codigo_ine'),
        Index('ix_gis_provincia_nombre', 'nombre_oficial'),
        Index('ix_gis_provincia_ccaa', 'comunidad_autonoma_id'),
    )

    def __repr__(self) -> str:
        return f"<Provincia {self.codigo_ine} - {self.nombre_oficial}>"


class Municipio(UUIDPKMixin, AuditMixin, GISBase):
    """
    Municipality of Spain (Municipio)
    
    Third-level administrative division (local government).
    Lives in GIS schema as geographic reference data.
    """
    __tablename__ = "municipios"
    
    codigo_ine: Mapped[str] = mapped_column(
        String(5), 
        unique=True, 
        index=True, 
        nullable=False,
        comment="INE official code (5 digits: 2 province + 3 municipality)"
    )
    codigo_ine_7: Mapped[Optional[str]] = mapped_column(
        String(7), 
        unique=True, 
        index=True,
        comment="Extended INE code with check digits"
    )
    nombre_oficial: Mapped[str] = mapped_column(
        String(100), 
        index=True, 
        nullable=False,
        comment="Official name"
    )
    nombre_cooficial: Mapped[Optional[str]] = mapped_column(
        String(100),
        comment="Co-official name in regional language"
    )
    nombre_alternativo: Mapped[Optional[str]] = mapped_column(
        String(100),
        comment="Alternative or historical name"
    )
    
    # Foreign key to parent geographic entity (same schema)
    provincia_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("gis.provincias.id"), 
        index=True, 
        nullable=False
    )
    
    # Relationships
    provincia: Mapped["Provincia"] = relationship(
        "Provincia", 
        back_populates="municipios"
    )
    
    # Cross-schema relationships to APP schema
    # These are 1:M relationships with descriptive names
    inmuebles: Mapped[list["Inmueble"]] = relationship(
        "Inmueble", 
        back_populates="municipio"
    )
    administraciones: Mapped[list["Administracion"]] = relationship(
        "Administracion", 
        back_populates="municipio_sede"
    )
    privados: Mapped[list["Privado"]] = relationship(
        "Privado", 
        back_populates="municipio_residencia"
    )
    tecnicos: Mapped[list["Tecnico"]] = relationship(
        "Tecnico", 
        back_populates="municipio_trabajo"
    )
    notarias: Mapped[list["Notaria"]] = relationship(
        "Notaria", 
        back_populates="municipio_ubicacion"
    )
    registros_propiedad: Mapped[list["RegistroPropiedad"]] = relationship(
        "RegistroPropiedad", 
        back_populates="municipio_ubicacion"
    )
    colegios_profesionales: Mapped[list["ColegioProfesional"]] = relationship(
        "ColegioProfesional", 
        back_populates="municipio_sede"
    )
    agencias_inmobiliarias: Mapped[list["AgenciaInmobiliaria"]] = relationship(
        "AgenciaInmobiliaria", 
        back_populates="municipio_oficina"
    )
    diocesis: Mapped[list["Diocesis"]] = relationship(
        "Diocesis", 
        back_populates="municipio_sede"
    )
    entidades_religiosas: Mapped[list["EntidadReligiosa"]] = relationship(
        "EntidadReligiosa", 
        back_populates="municipio_sede"
    )
    
    __table_args__ = (
        Index('ix_gis_municipio_codigo_ine', 'codigo_ine'),
        Index('ix_gis_municipio_nombre', 'nombre_oficial'),
        Index('ix_gis_municipio_provincia', 'provincia_id'),
    )

    def __repr__(self) -> str:
        return f"<Municipio {self.codigo_ine} - {self.nombre_oficial}>"
