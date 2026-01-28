# models/actores/administraciones.py
"""
Public Administration Actors and Entities

This module contains models related to public administrations at all levels
(national, regional, provincial, local) and their organizational hierarchies.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey

from sipi.db.base import AppBase
from sipi.db.mixins import (
    UUIDPKMixin, 
    AuditMixin, 
    ContactoDireccionMixin,
    TitularidadMixin
)
from ._base import TitularBase


class Administracion(UUIDPKMixin, AuditMixin, ContactoDireccionMixin, 
                     TitularidadMixin, AppBase):
    """
    Public Administration (Administración Pública)
    
    Represents any level of public administration in Spain:
    - National (Estado)
    - Regional (Comunidad Autónoma)
    - Provincial (Diputación)
    - Local (Ayuntamiento)
    
    Supports hierarchical organization with parent-child relationships
    and temporal validity for handling administrative restructuring.
    """
    __tablename__ = "administraciones"

    nombre: Mapped[str] = mapped_column(
        String(255), 
        index=True,
        comment="Official name of the administration"
    )
    codigo_oficial: Mapped[Optional[str]] = mapped_column(
        String(100), 
        unique=True, 
        index=True,
        comment="Official administrative code (e.g., DIR3)"
    )
    ambito: Mapped[Optional[str]] = mapped_column(
        String(100),
        comment="Scope or jurisdiction of the administration"
    )

    # Hierarchical Organization
    administracion_padre_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("app.administraciones.id"), 
        index=True,
        comment="Parent administration in the hierarchy"
    )
    nivel_jerarquico: Mapped[Optional[str]] = mapped_column(
        String(50), 
        index=True,
        comment="Hierarchical level: ESTATAL, AUTONOMICO, PROVINCIAL, LOCAL"
    )
    tipo_organo: Mapped[Optional[str]] = mapped_column(
        String(100), 
        index=True,
        comment="Type of administrative body: CONSEJERIA, DIRECCION_GENERAL, SERVICIO, etc."
    )
    orden_jerarquico: Mapped[Optional[int]] = mapped_column(
        index=True,
        comment="Order within the same hierarchical level"
    )

    # Temporal Validity (for handling restructuring)
    valido_desde: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, 
        index=True,
        comment="Start date of validity"
    )
    valido_hasta: Mapped[Optional[datetime]] = mapped_column(
        nullable=True, 
        index=True,
        comment="End date of validity (null if currently active)"
    )
    activa: Mapped[bool] = mapped_column(
        Boolean, 
        default=True, 
        index=True,
        comment="Whether the administration is currently active"
    )

    # Note: Geographic FKs come from ContactoDireccionMixin
    # (comunidad_autonoma_id, provincia_id, municipio_id)

    # Relationships
    # Cross-schema relationships to GIS schema
    comunidad_autonoma: Mapped[Optional["ComunidadAutonoma"]] = relationship(
        "ComunidadAutonoma",
        primaryjoin="foreign(Administracion.comunidad_autonoma_id) == ComunidadAutonoma.id",
        back_populates="administraciones",
        doc="Autonomous community where this administration operates"
    )
    provincia: Mapped[Optional["Provincia"]] = relationship(
        "Provincia",
        primaryjoin="foreign(Administracion.provincia_id) == Provincia.id",
        back_populates="administraciones",
        doc="Province where this administration operates"
    )
    municipio_sede: Mapped[Optional["Municipio"]] = relationship(
        "Municipio",
        primaryjoin="foreign(Administracion.municipio_id) == Municipio.id",
        back_populates="administraciones",
        doc="Municipality where the administration headquarters is located"
    )

    # Hierarchical relationships (self-referential)
    administracion_padre: Mapped[Optional["Administracion"]] = relationship(
        "Administracion",
        remote_side="Administracion.id",
        foreign_keys=[administracion_padre_id],
        back_populates="subadministraciones",
        doc="Parent administration in the organizational hierarchy"
    )
    subadministraciones: Mapped[list["Administracion"]] = relationship(
        "Administracion",
        back_populates="administracion_padre",
        cascade="all, delete-orphan",
        doc="Child administrations in the organizational hierarchy"
    )

    # Relationships within APP schema
    titulares: Mapped[list["AdministracionTitular"]] = relationship(
        "AdministracionTitular", 
        back_populates="administracion", 
        cascade="all, delete-orphan",
        doc="Administrators who have managed this administration over time"
    )
    subvenciones: Mapped[list["SubvencionAdministracion"]] = relationship(
        "SubvencionAdministracion", 
        back_populates="administracion",
        doc="Subsidies granted by this administration"
    )

    def __repr__(self) -> str:
        return f"<Administracion {self.codigo_oficial} - {self.nombre}>"


class AdministracionTitular(TitularBase, ContactoDireccionMixin):
    """
    Administration Manager (Responsable de Administración)
    
    Represents a person who manages or is responsible for a public
    administration during a specific period (e.g., mayor, director, etc.).
    """
    __tablename__ = "administraciones_titulares"

    administracion_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("app.administraciones.id"), 
        index=True,
        comment="Reference to the administration"
    )

    # Relationships
    administracion: Mapped["Administracion"] = relationship(
        "Administracion", 
        back_populates="titulares",
        doc="The administration managed by this person"
    )

    def __repr__(self) -> str:
        return f"<AdministracionTitular {self.nombre} - {self.cargo}>"
