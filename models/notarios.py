# models/actores/notarias.py
from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from db.registry import Base
from mixins import UUIDPKMixin, AuditMixin, ContactoDireccionMixin
from .actores_base import TitularBase

if TYPE_CHECKING:
    from models.geografia import Municipio
    from models.transmisiones import Transmision

class Notaria(UUIDPKMixin, AuditMixin, ContactoDireccionMixin, Base):
    __tablename__ = "notarias"

    codigo_oficial: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), index=True)
    municipio_ubicacion: Mapped[Optional["Municipio"]] = relationship(
        "Municipio",
        primaryjoin="foreign(Notaria.municipio_id) == Municipio.id",
        back_populates="notarias",
    )

    transmisiones: Mapped[list["Transmision"]] = relationship(
        "Transmision",
        back_populates="notaria",
    )
    titulares: Mapped[list["NotariaTitular"]] = relationship(
        "NotariaTitular",
        back_populates="notaria",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Notaria {self.codigo_oficial} - {self.nombre}>"

class NotariaTitular(TitularBase):
    __tablename__ = "notarias_titulares"

    notaria_id: Mapped[str] = mapped_column(String(36), ForeignKey("app.notarias.id"), index=True)

    notaria: Mapped["Notaria"] = relationship(
        "Notaria",
        back_populates="titulares",
    )

    def __repr__(self) -> str:
        return f"<NotariaTitular {self.nombre} - {self.notaria_id}>"

