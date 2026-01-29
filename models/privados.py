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

from db.registry import   Base
from mixins import (
    UUIDPKMixin, 
    AuditMixin, 
    ContactoDireccionMixin
)
from .actores_base import PersonaMixin


class Privado(UUIDPKMixin, AuditMixin, PersonaMixin, 
              ContactoDireccionMixin, Base):
    
    __tablename__ = "privados"

    # Note: nombre, apellidos, nif, etc. come from PersonaMixin
    # municipio_id comes from ContactoDireccionMixin
    
    municipio_residencia: Mapped[Optional["Municipio"]] = relationship(
        "Municipio",
        primaryjoin="foreign(Privado.municipio_id) == Municipio.id",
        back_populates="privados",
        doc="Municipality of residence for this private actor"
    )

    def __repr__(self) -> str:
        return f"<Privado {self.nif} - {self.nombre}>"


