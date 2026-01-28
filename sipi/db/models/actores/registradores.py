# models/actores/registradores.py
"""
Property Registry Actors and Entities

This module contains models related to property registrars and property
registries, which maintain official records of property ownership and rights.
"""

from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from sipi.db.base import AppBase
from sipi.db.mixins import (
    UUIDPKMixin, 
    AuditMixin, 
    IdentificacionMixin,
    ContactoDireccionMixin,
    TitularidadMixin
)
from ._base import TitularBase


class RegistroPropiedad(UUIDPKMixin, AuditMixin, IdentificacionMixin, 
                        ContactoDireccionMixin, TitularidadMixin, AppBase):
    """
    Property Registry (Registro de la Propiedad)
    
    Official registry that maintains records of property ownership,
    mortgages, liens, and other property rights. Each registry has
    jurisdiction over specific geographic areas.
    """
    __tablename__ = "registros_propiedad"
    
    # Note: nombre and codigo_oficial come from IdentificacionMixin
    # municipio_id comes from ContactoDireccionMixin
    
    # Relationships
    # Cross-schema relationship to GIS schema
    municipio_ubicacion: Mapped[Optional["Municipio"]] = relationship(
        "Municipio",
        primaryjoin="foreign(RegistroPropiedad.municipio_id) == Municipio.id",
        back_populates="registros_propiedad",
        doc="Municipality where the property registry is located"
    )
    
    # Relationships within APP schema
    transmisiones: Mapped[list["Transmision"]] = relationship(
        "Transmision", 
        back_populates="registro_propiedad",
        doc="Property transmissions registered in this registry"
    )
    inmatriculaciones: Mapped[list["Inmatriculacion"]] = relationship(
        "Inmatriculacion", 
        back_populates="registro_propiedad",
        doc="Property registrations (inmatriculaciones) in this registry"
    )
    titulares: Mapped[list["RegistroPropiedadTitular"]] = relationship(
        "RegistroPropiedadTitular", 
        back_populates="registro_propiedad", 
        cascade="all, delete-orphan",
        doc="Registrars who have held this registry over time"
    )

    def __repr__(self) -> str:
        return f"<RegistroPropiedad {self.codigo_oficial} - {self.nombre}>"


class RegistroPropiedadTitular(TitularBase):
    """
    Property Registrar (Registrador de la Propiedad)
    
    Represents a property registrar (physical person) who manages a
    property registry during a specific period. Registrars are legal
    professionals responsible for maintaining property records.
    """
    __tablename__ = "registros_propiedad_titulares"
    
    registro_propiedad_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("app.registros_propiedad.id"), 
        index=True,
        comment="Reference to the property registry"
    )
    
    # Relationships
    registro_propiedad: Mapped["RegistroPropiedad"] = relationship(
        "RegistroPropiedad", 
        back_populates="titulares",
        doc="The property registry managed by this registrar"
    )

    def __repr__(self) -> str:
        return f"<RegistroPropiedadTitular {self.nombre} - {self.registro_propiedad_id}>"
