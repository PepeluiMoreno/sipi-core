# models/actores/notarios.py
"""
Notarial Actors and Entities

This module contains models related to notaries and notarial offices,
which are responsible for authenticating legal documents and transactions.
"""

from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from sipi.db.base import AppBase
from sipi.db.mixins import (
    UUIDPKMixin, 
    AuditMixin, 
    ContactoDireccionMixin
)
from ._base import TitularBase


class Notaria(UUIDPKMixin, AuditMixin, ContactoDireccionMixin, AppBase):
    """
    Notarial Office (Notaría)
    
    Represents a notarial office where notaries practice.
    Each notary office has a unique official code and can have
    multiple notaries over time (managed through NotariaTitular).
    """
    __tablename__ = "notarias"
    
    nombre: Mapped[str] = mapped_column(
        String(255), 
        index=True,
        comment="Name of the notarial office"
    )
    codigo_oficial: Mapped[str] = mapped_column(
        String(20), 
        unique=True, 
        index=True, 
        nullable=False,
        comment="Official notary code assigned by the government"
    )

    # Relationships
    # Note: municipio_id comes from ContactoDireccionMixin
    # Cross-schema relationship to GIS schema
    municipio_ubicacion: Mapped[Optional["Municipio"]] = relationship(
        "Municipio",
        primaryjoin="foreign(Notaria.municipio_id) == Municipio.id",
        back_populates="notarias",
        doc="Municipality where the notarial office is located"
    )
    
    # Relationships within APP schema
    transmisiones: Mapped[list["Transmision"]] = relationship(
        "Transmision", 
        back_populates="notaria",
        doc="Property transmissions authenticated by this notary office"
    )
    titulares: Mapped[list["NotariaTitular"]] = relationship(
        "NotariaTitular", 
        back_populates="notaria", 
        cascade="all, delete-orphan",
        doc="Notaries who have held this office over time"
    )

    def __repr__(self) -> str:
        return f"<Notaria {self.codigo_oficial} - {self.nombre}>"


class NotariaTitular(TitularBase):
    """
    Notary Holder (Notario Titular)
    
    Represents a notary (physical person) who holds a notarial office
    during a specific period. A notary office can have different notaries
    over time, and this table tracks the temporal relationship.
    """
    __tablename__ = "notarias_titulares"
    
    notaria_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("app.notarias.id"), 
        index=True,
        comment="Reference to the notarial office"
    )
    
    # Relationships
    notaria: Mapped["Notaria"] = relationship(
        "Notaria", 
        back_populates="titulares",
        doc="The notarial office held by this notary"
    )

    def __repr__(self) -> str:
        return f"<NotariaTitular {self.nombre} - {self.notaria_id}>"
