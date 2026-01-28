# models/actores/_base.py
"""
Base Classes and Mixins for Actor Models

This module provides common base classes and mixins used across
all actor types in the application.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from ..base import AppBase
from ...mixins import (
    UUIDPKMixin, 
    AuditMixin, 
    IdentificacionMixin
)


class PersonaMixin(IdentificacionMixin):
    """
    Base mixin for physical and legal persons
    
    Provides common identification fields for all person types.
    """
    tipo_persona_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("app.tipos_persona.id"), 
        index=True,
        comment="Reference to person type (physical/legal)"
    )


class TitularBase(UUIDPKMixin, AuditMixin, IdentificacionMixin, AppBase):
    """
    Base class for temporary holder/manager tables
    
    Used for entities that have time-bound managers or holders
    (e.g., notaries, registrars, bishops, administrators).
    """
    __abstract__ = True
    
    fecha_inicio: Mapped[datetime] = mapped_column(
        index=True,
        comment="Start date of tenure"
    )
    fecha_fin: Mapped[Optional[datetime]] = mapped_column(
        index=True,
        comment="End date of tenure (null if current)"
    )
    cargo: Mapped[Optional[str]] = mapped_column(
        String(100),
        comment="Position or title held"
    )
