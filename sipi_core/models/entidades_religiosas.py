# models/actores/entidades_religiosas.py
from __future__ import annotations

from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey

from db.registry import Base
from mixins import (
    UUIDPKMixin,
    AuditMixin,
    IdentificacionMixin,
    ContactoDireccionMixin,
    TitularidadMixin,
)
from models.actores_base import TitularBase

if TYPE_CHECKING:
    from models.geografia import Municipio
    from models.inmuebles import Inmueble
    from models.tipologias import TipoEntidadReligiosa


class Diocesis(
    UUIDPKMixin,
    AuditMixin,
    ContactoDireccionMixin,
    TitularidadMixin,
    Base,
):
    __tablename__ = "diocesis"

    nombre: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    wikidata_qid: Mapped[Optional[str]] = mapped_column(String(32), unique=True, index=True)

    municipio_sede: Mapped[Optional["Municipio"]] = relationship(
        "Municipio",
        primaryjoin="foreign(Diocesis.municipio_id) == Municipio.id",
        back_populates="diocesis",
    )

    inmuebles: Mapped[list["Inmueble"]] = relationship(
        "Inmueble",
        back_populates="diocesis",
    )
    titulares: Mapped[list["DiocesisTitular"]] = relationship(
        "DiocesisTitular",
        back_populates="diocesis",
        cascade="all, delete-orphan",
    )


class DiocesisTitular(TitularBase, Base):
    __tablename__ = "diocesis_titulares"

    diocesis_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("app.diocesis.id"),
        index=True,
    )

    diocesis: Mapped["Diocesis"] = relationship(
        "Diocesis",
        back_populates="titulares",
    )


class EntidadReligiosa(
    UUIDPKMixin,
    AuditMixin,
    IdentificacionMixin,
    ContactoDireccionMixin,
    TitularidadMixin,
    Base,
):
    __tablename__ = "entidades_religiosas"

    numero_registro: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )
    tipo_entidad_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("app.tipos_entidad_religiosa.id", ondelete="RESTRICT"),
        index=True,
    )
    fecha_fundacion: Mapped[Optional[datetime]] = mapped_column()
    activa: Mapped[bool] = mapped_column(Boolean, default=True)

    tipo_entidad: Mapped[Optional["TipoEntidadReligiosa"]] = relationship(
        "TipoEntidadReligiosa",
        back_populates="entidades_religiosas",
    )
    municipio_sede: Mapped[Optional["Municipio"]] = relationship(
        "Municipio",
        primaryjoin="foreign(EntidadReligiosa.municipio_id) == Municipio.id",
        back_populates="entidades_religiosas",
    )

    inmuebles: Mapped[list["Inmueble"]] = relationship(
        "Inmueble",
        back_populates="entidad_religiosa",
    )
    titulares: Mapped[list["EntidadReligiosaTitular"]] = relationship(
        "EntidadReligiosaTitular",
        back_populates="entidad_religiosa",
        cascade="all, delete-orphan",
    )


class EntidadReligiosaTitular(TitularBase, Base):
    __tablename__ = "entidades_religiosas_titulares"

    entidad_religiosa_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("app.entidades_religiosas.id", ondelete="CASCADE"),
        index=True,
    )

    entidad_religiosa: Mapped["EntidadReligiosa"] = relationship(
        "EntidadReligiosa",
        back_populates="titulares",
    )

