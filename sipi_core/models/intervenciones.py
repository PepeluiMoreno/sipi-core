# models/intervenciones.py
from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, Numeric

from db.registry import Base
from mixins import UUIDPKMixin, AuditMixin

class Intervencion(UUIDPKMixin, AuditMixin, Base):
    """Intervenciones arquitectónicas realizadas sobre un inmueble"""
    __tablename__ = "intervenciones"

    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("app.inmuebles.id"), index=True)
    nombre: Mapped[str] = mapped_column(String(255), index=True)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    # Fechas
    fecha_inicio: Mapped[Optional[datetime]] = mapped_column(index=True)
    fecha_fin: Mapped[Optional[datetime]] = mapped_column(index=True)

    # Presupuesto
    presupuesto: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2))

    # Relaciones
    inmueble: Mapped["Inmueble"] = relationship("Inmueble", back_populates="intervenciones")
    tecnicos: Mapped[list["IntervencionTecnico"]] = relationship("IntervencionTecnico", back_populates="intervencion", cascade="all, delete-orphan")
    subvenciones: Mapped[list["IntervencionSubvencion"]] = relationship("IntervencionSubvencion", back_populates="intervencion", cascade="all, delete-orphan")

class IntervencionTecnico(UUIDPKMixin, AuditMixin, Base):
    """Técnicos asignados a una intervención con roles específicos"""
    __tablename__ = "intervenciones_tecnicos"

    intervencion_id: Mapped[str] = mapped_column(String(36), ForeignKey("app.intervenciones.id"), index=True)
    tecnico_id: Mapped[str] = mapped_column(String(36), ForeignKey("app.tecnicos.id"), index=True)
    rol_tecnico_id: Mapped[str] = mapped_column(String(36), ForeignKey("app.roles_tecnico.id"), index=True)

    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    fecha_inicio: Mapped[Optional[datetime]] = mapped_column(index=True)
    fecha_fin: Mapped[Optional[datetime]] = mapped_column(index=True)

    # Relaciones
    intervencion: Mapped["Intervencion"] = relationship("Intervencion", back_populates="tecnicos")
    tecnico: Mapped["Tecnico"] = relationship("Tecnico", back_populates="intervenciones")
    rol_tecnico: Mapped["TipoRolTecnico"] = relationship("TipoRolTecnico", lazy="joined")
