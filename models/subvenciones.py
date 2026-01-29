# models/subvenciones.py
from __future__ import annotations
from typing import TYPE_CHECKING
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Numeric, ForeignKey

from db.registry import Base
from mixins import UUIDPKMixin, AuditMixin

if TYPE_CHECKING:
    from models.intervenciones import Intervencion
    from models.administraciones import Administracion


class IntervencionSubvencion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "intervenciones_subvenciones"

    intervencion_id: Mapped[str] = mapped_column(String(36), ForeignKey("app.intervenciones.id"), index=True)
    codigo_concesion: Mapped[str] = mapped_column(String(100), index=True)
    importe_aplicado: Mapped[Decimal | None] = mapped_column(Numeric(15, 2), nullable=True)
    porcentaje_financiacion: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    justificacion_gasto: Mapped[str | None] = mapped_column(Text, nullable=True)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relaciones
    intervencion: Mapped["Intervencion"] = relationship("Intervencion", back_populates="subvenciones")
    administraciones: Mapped[list["SubvencionAdministracion"]] = relationship("SubvencionAdministracion", back_populates="subvencion", cascade="all, delete-orphan")

class SubvencionAdministracion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "subvenciones_administraciones"

    subvencion_id: Mapped[str] = mapped_column(String(36), ForeignKey("app.intervenciones_subvenciones.id"), index=True)
    administracion_id: Mapped[str] = mapped_column(String(36), ForeignKey("app.administraciones.id"), index=True)
    importe_aportado: Mapped[Decimal | None] = mapped_column(Numeric(15, 2), nullable=True)
    porcentaje_participacion: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)

    # Relaciones
    subvencion: Mapped["IntervencionSubvencion"] = relationship("IntervencionSubvencion", back_populates="administraciones")
    administracion: Mapped["Administracion"] = relationship("Administracion", back_populates="subvenciones")
