# models/actores/privados.py
"""
Private Actors and Commercial Entities

This module contains models related to private individuals and
commercial entities involved in property transactions.
"""

from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from db.models.base import AppBase
from db.mixins import (
    UUIDPKMixin, 
    AuditMixin, 
    ContactoDireccionMixin
)
from ._base import PersonaMixin


class Privado(UUIDPKMixin, AuditMixin, PersonaMixin, 
              ContactoDireccionMixin, AppBase):
    """
    Private Individual or Entity (Privado)
    
    Represents private actors in property transactions:
    - Physical persons (individuals)
    - Legal persons (companies, foundations, etc.)
    
    These can act as:
    - Property owners
    - Buyers
    - Sellers
    - Usufructuaries
    - etc.
    """
    __tablename__ = "privados"

    # Note: nombre, apellidos, nif, etc. come from PersonaMixin
    # municipio_id comes from ContactoDireccionMixin
    
    # Relationships
    # Cross-schema relationship to GIS schema
    municipio_residencia: Mapped[Optional["Municipio"]] = relationship(
        "Municipio",
        primaryjoin="foreign(Privado.municipio_id) == Municipio.id",
        back_populates="privados",
        doc="Municipality of residence for this private actor"
    )

    def __repr__(self) -> str:
        return f"<Privado {self.nif} - {self.nombre}>"


class AgenciaInmobiliaria(UUIDPKMixin, AuditMixin, ContactoDireccionMixin, AppBase):
    """
    Real Estate Agency (Agencia Inmobiliaria)
    
    Represents real estate agencies that advertise and facilitate
    property transactions.
    """
    __tablename__ = "agencias_inmobiliarias"
    
    nombre: Mapped[str] = mapped_column(
        String(255), 
        index=True,
        comment="Name of the real estate agency"
    )
    
    # Relationships
    # Cross-schema relationship to GIS schema
    municipio_oficina: Mapped[Optional["Municipio"]] = relationship(
        "Municipio",
        primaryjoin="foreign(AgenciaInmobiliaria.municipio_id) == Municipio.id",
        back_populates="agencias_inmobiliarias",
        doc="Municipality where the agency office is located"
    )
    
    # Relationships within APP schema
    transmisiones_anunciadas: Mapped[list["TransmisionAnunciante"]] = relationship(
        "TransmisionAnunciante", 
        back_populates="agencia_inmobiliaria",
        doc="Property transmissions advertised by this agency"
    )

    def __repr__(self) -> str:
        return f"<AgenciaInmobiliaria {self.nombre}>"
