# models/actores/tecnicos.py
"""
Technical Professionals and Professional Associations

This module contains models related to technical professionals
(architects, engineers, etc.) and their professional associations.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from sipi.db.base import AppBase
from sipi.db.mixins import (
    UUIDPKMixin, 
    AuditMixin, 
    IdentificacionMixin,
    ContactoDireccionMixin
)


class Tecnico(UUIDPKMixin, AuditMixin, IdentificacionMixin, 
              ContactoDireccionMixin, AppBase):
    """
    Technical Professional (Técnico)
    
    Represents technical professionals such as architects, engineers,
    surveyors, and other professionals involved in property interventions.
    """
    __tablename__ = "tecnicos"
    
    # Foreign Keys
    rol_tecnico_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("app.roles_tecnico.id"), 
        index=True,
        comment="Technical role (architect, engineer, etc.)"
    )
    colegio_profesional_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("app.colegios_profesionales.id"), 
        index=True,
        comment="Professional association membership"
    )
    
    # Professional Information
    numero_colegiado: Mapped[Optional[str]] = mapped_column(
        String(50), 
        index=True,
        comment="Professional association membership number"
    )
    fecha_colegiacion: Mapped[Optional[datetime]] = mapped_column(
        comment="Date of professional association membership"
    )
    
    # Relationships
    rol_tecnico: Mapped[Optional["TipoRolTecnico"]] = relationship(
        "TipoRolTecnico", 
        back_populates="tecnicos",
        doc="Technical role classification"
    )
    colegio_profesional: Mapped[Optional["ColegioProfesional"]] = relationship(
        "ColegioProfesional", 
        back_populates="tecnicos",
        doc="Professional association this technician belongs to"
    )
    
    # Cross-schema relationship to GIS schema
    municipio_trabajo: Mapped[Optional["Municipio"]] = relationship(
        "Municipio", 
        primaryjoin="foreign(Tecnico.municipio_id) == Municipio.id",
        back_populates="tecnicos",
        doc="Municipality where the technician primarily works"
    )
    
    # Relationships within APP schema
    intervenciones: Mapped[list["IntervencionTecnico"]] = relationship(
        "IntervencionTecnico", 
        back_populates="tecnico",
        doc="Property interventions performed by this technician"
    )

    def __repr__(self) -> str:
        return f"<Tecnico {self.numero_colegiado} - {self.nombre}>"


class ColegioProfesional(UUIDPKMixin, AuditMixin, ContactoDireccionMixin, AppBase):
    """
    Professional Association (Colegio Profesional)
    
    Represents professional associations such as:
    - Colegio de Arquitectos (Architects' Association)
    - Colegio de Ingenieros (Engineers' Association)
    - etc.
    
    These associations regulate professional practice and maintain
    registries of qualified professionals.
    """
    __tablename__ = "colegios_profesionales"
    
    nombre: Mapped[str] = mapped_column(
        String(255), 
        unique=True, 
        index=True,
        comment="Official name of the professional association"
    )
    codigo: Mapped[Optional[str]] = mapped_column(
        String(50), 
        unique=True, 
        index=True,
        comment="Official code of the association"
    )
    
    # Relationships
    # Cross-schema relationship to GIS schema
    municipio_sede: Mapped[Optional["Municipio"]] = relationship(
        "Municipio", 
        primaryjoin="foreign(ColegioProfesional.municipio_id) == Municipio.id",
        back_populates="colegios_profesionales",
        doc="Municipality where the association headquarters is located"
    )
    
    # Relationships within APP schema
    tecnicos: Mapped[list["Tecnico"]] = relationship(
        "Tecnico", 
        back_populates="colegio_profesional",
        doc="Professionals registered with this association"
    )

    def __repr__(self) -> str:
        return f"<ColegioProfesional {self.codigo} - {self.nombre}>"
