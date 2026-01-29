# models/administraciones.py

from __future__ import annotations

from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.registry import Base
from mixins import (
    UUIDPKMixin,
    AuditMixin,
    ContactoDireccionMixin,
    TitularidadMixin,
)
from .actores_base import TitularBase

if TYPE_CHECKING:
    from models.geografia import ComunidadAutonoma, Provincia, Municipio
    from models.subvenciones import SubvencionAdministracion

class Administracion(
    UUIDPKMixin,
    AuditMixin,
    ContactoDireccionMixin,
    TitularidadMixin,
    Base,
):
    __tablename__ = "administraciones"
    __table_args__ = {"schema": "app"}  

    nombre: Mapped[str] = mapped_column(String(255), index=True)
    codigo_oficial: Mapped[Optional[str]] = mapped_column(
        String(100), unique=True, index=True
    )
    ambito: Mapped[Optional[str]] = mapped_column(String(100))

    # Auto-referencia: usar schema explícito
    administracion_padre_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("app.administraciones.id"),  # Schema explícito
        index=True,
    )
    
    # ... resto igual ...
    nivel_jerarquico: Mapped[Optional[str]] = mapped_column(
        String(50),
        index=True,
    )
    tipo_organo: Mapped[Optional[str]] = mapped_column(
        String(100),
        index=True,
    )
    orden_jerarquico: Mapped[Optional[int]] = mapped_column(index=True)

    valido_desde: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        index=True,
    )
    valido_hasta: Mapped[Optional[datetime]] = mapped_column(
        nullable=True,
        index=True,
    )
    activa: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        index=True,
    )

    comunidad_autonoma: Mapped[Optional["ComunidadAutonoma"]] = relationship(
        "ComunidadAutonoma",
        back_populates="administraciones",
    )
    provincia: Mapped[Optional["Provincia"]] = relationship(
        "Provincia",
        back_populates="administraciones",
    )
    municipio_sede: Mapped[Optional["Municipio"]] = relationship(
        "Municipio",
        back_populates="administraciones",
    )

    administracion_padre: Mapped[Optional["Administracion"]] = relationship(
        "Administracion",
        remote_side="Administracion.id",
        foreign_keys=[administracion_padre_id],
        back_populates="subadministraciones",
    )
    subadministraciones: Mapped[list["Administracion"]] = relationship(
        "Administracion",
        back_populates="administracion_padre",
        cascade="all, delete-orphan",
    )

    titulares: Mapped[list["AdministracionTitular"]] = relationship(
        "AdministracionTitular",
        back_populates="administracion",
        cascade="all, delete-orphan",
    )
    subvenciones: Mapped[list["SubvencionAdministracion"]] = relationship(
        "SubvencionAdministracion",
        back_populates="administracion",
    )

    def __repr__(self) -> str:
        return f"<Administracion {self.codigo_oficial} - {self.nombre}>"


class AdministracionTitular(TitularBase, ContactoDireccionMixin, Base):
    __tablename__ = "administraciones_titulares"

    administracion_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("app.administraciones.id"),
        index=True,
    )

    administracion: Mapped["Administracion"] = relationship(
        "Administracion",
        back_populates="titulares",
    )

    def __repr__(self) -> str:
        return f"<AdministracionTitular {self.nombre} - {self.cargo}>"

