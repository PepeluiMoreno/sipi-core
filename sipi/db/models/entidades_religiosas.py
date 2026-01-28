# models/actores/entidades_religiosas.py
"""
Religious Entities and Ecclesiastical Actors

This module contains models related to religious organizations including
dioceses, religious orders, congregations, and other ecclesiastical entities.
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
    IdentificacionMixin,
    ContactoDireccionMixin,
    TitularidadMixin
)
from .actores_base import TitularBase


class Diocesis(UUIDPKMixin, AuditMixin, ContactoDireccionMixin, 
               TitularidadMixin, AppBase):
    """
    Catholic Diocese (Diócesis)
    
    Represents a Catholic diocese, which is a territorial division
    of the Catholic Church under the authority of a bishop.
    """
    __tablename__ = "diocesis"
    
    nombre: Mapped[str] = mapped_column(
        String(100), 
        unique=True, 
        index=True,
        comment="Official name of the diocese"
    )
    wikidata_qid: Mapped[Optional[str]] = mapped_column(
        String(32), 
        unique=True, 
        index=True,
        comment="Wikidata identifier (Q-number)"
    )
    
    # Relationships
    # Cross-schema relationship to GIS schema
    municipio_sede: Mapped[Optional["Municipio"]] = relationship(
        "Municipio", 
        primaryjoin="foreign(Diocesis.municipio_id) == Municipio.id",
        back_populates="diocesis",
        doc="Municipality where the diocesan cathedral is located"
    )
    
    # Relationships within APP schema
    inmuebles: Mapped[list["Inmueble"]] = relationship(
        "Inmueble", 
        back_populates="diocesis",
        doc="Properties within the geographic jurisdiction of this diocese"
    )
    titulares: Mapped[list["DiocesisTitular"]] = relationship(
        "DiocesisTitular", 
        back_populates="diocesis", 
        cascade="all, delete-orphan",
        doc="Bishops who have led this diocese over time"
    )

    def __repr__(self) -> str:
        return f"<Diocesis {self.nombre}>"


class DiocesisTitular(TitularBase):
    """
    Bishop (Obispo)
    
    Represents a bishop who leads a diocese during a specific period.
    """
    __tablename__ = "diocesis_titulares"
    
    diocesis_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("app.diocesis.id"), 
        index=True,
        comment="Reference to the diocese"
    )
    
    # Relationships
    diocesis: Mapped["Diocesis"] = relationship(
        "Diocesis", 
        back_populates="titulares",
        doc="The diocese led by this bishop"
    )

    def __repr__(self) -> str:
        return f"<DiocesisTitular {self.nombre} - {self.diocesis_id}>"


class EntidadReligiosa(UUIDPKMixin, AuditMixin, IdentificacionMixin, 
                       ContactoDireccionMixin, TitularidadMixin, AppBase):
    """
    Religious Entity (Entidad Religiosa)
    
    Represents religious organizations such as:
    - Religious orders (Órdenes religiosas)
    - Congregations (Congregaciones)
    - Institutes of Consecrated Life (Institutos de Vida Consagrada)
    - Other ecclesiastical entities
    
    These entities can own and manage properties.
    """
    __tablename__ = "entidades_religiosas"

    numero_registro: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment="Official registration number in the Registry of Religious Entities"
    )

    tipo_entidad_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("app.tipos_entidad_religiosa.id", ondelete="RESTRICT"), 
        index=True,
        comment="Type of religious entity (order, congregation, etc.)"
    )
    fecha_fundacion: Mapped[Optional[datetime]] = mapped_column(
        comment="Foundation date of the entity"
    )
    activa: Mapped[bool] = mapped_column(
        Boolean, 
        default=True,
        comment="Whether the entity is currently active"
    )

    # Relationships
    # Cross-schema relationship to GIS schema
    tipo_entidad: Mapped[Optional["TipoEntidadReligiosa"]] = relationship(
        "TipoEntidadReligiosa", 
        back_populates="entidades_religiosas",
        doc="Type classification of this religious entity"
    )
    municipio_sede: Mapped[Optional["Municipio"]] = relationship(
        "Municipio",
        primaryjoin="foreign(EntidadReligiosa.municipio_id) == Municipio.id",
        back_populates="entidades_religiosas",
        doc="Municipality where the entity's headquarters is located"
    )
    
    # Relationships within APP schema
    inmuebles: Mapped[list["Inmueble"]] = relationship(
        "Inmueble", 
        back_populates="entidad_religiosa",
        doc="Properties owned or managed by this religious entity"
    )
    titulares: Mapped[list["EntidadReligiosaTitular"]] = relationship(
        "EntidadReligiosaTitular", 
        back_populates="entidad_religiosa", 
        cascade="all, delete-orphan",
        doc="Leaders who have managed this entity over time"
    )

    def __repr__(self) -> str:
        return f"<EntidadReligiosa {self.numero_registro} - {self.nombre}>"


class EntidadReligiosaTitular(TitularBase):
    """
    Religious Entity Leader (Responsable de Entidad Religiosa)
    
    Represents a person who leads or manages a religious entity
    during a specific period (e.g., superior, prior, abbess, etc.).
    """
    __tablename__ = "entidades_religiosas_titulares"

    entidad_religiosa_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("app.entidades_religiosas.id", ondelete="CASCADE"), 
        index=True,
        comment="Reference to the religious entity"
    )

    # Relationships
    entidad_religiosa: Mapped["EntidadReligiosa"] = relationship(
        "EntidadReligiosa", 
        back_populates="titulares",
        doc="The religious entity led by this person"
    )

    def __repr__(self) -> str:
        return f"<EntidadReligiosaTitular {self.nombre} - {self.cargo}>"
