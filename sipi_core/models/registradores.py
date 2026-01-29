# models/actores/registradores.py
from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from db.registry import Base
from mixins import UUIDPKMixin, AuditMixin, IdentificacionMixin, ContactoDireccionMixin, TitularidadMixin
from models.actores_base import TitularBase

if TYPE_CHECKING:
    from models.geografia import Municipio
    from models.inmuebles import Inmatriculacion
    from models.transmisiones import Transmision

class RegistroPropiedad(
    UUIDPKMixin,
    AuditMixin,
    IdentificacionMixin,
    ContactoDireccionMixin,
    TitularidadMixin,
    Base
):
    __tablename__ = "registros_propiedad"

    municipio_ubicacion: Mapped[Optional["Municipio"]] = relationship(
        "Municipio",
        primaryjoin="foreign(RegistroPropiedad.municipio_id) == Municipio.id",
        back_populates="registros_propiedad",
    )

    transmisiones: Mapped[list["Transmision"]] = relationship(
        "Transmision",
        back_populates="registro_propiedad",
    )
    inmatriculaciones: Mapped[list["Inmatriculacion"]] = relationship(
        "Inmatriculacion",
        back_populates="registro_propiedad",
    )
    titulares: Mapped[list["RegistroPropiedadTitular"]] = relationship(
        "RegistroPropiedadTitular",
        back_populates="registro_propiedad",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<RegistroPropiedad {self.codigo_oficial} - {self.nombre}>"


class RegistroPropiedadTitular(TitularBase, Base):
    __tablename__ = "registros_propiedad_titulares"

    registro_propiedad_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("app.registros_propiedad.id"),
        index=True,
    )

    registro_propiedad: Mapped["RegistroPropiedad"] = relationship(
        "RegistroPropiedad",
        back_populates="titulares",
    )

    def __repr__(self) -> str:
        return f"<RegistroPropiedadTitular {self.nombre} - {self.registro_propiedad_id}>"
