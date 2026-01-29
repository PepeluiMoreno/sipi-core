
# models/agencias.py
from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from db.registry import Base
from mixins import UUIDPKMixin, AuditMixin, ContactoDireccionMixin

if TYPE_CHECKING:
    from models.geografia import Municipio
    from models.transmisiones import TransmisionAnunciante

class AgenciaInmobiliaria(UUIDPKMixin, AuditMixin, ContactoDireccionMixin, Base):
    __tablename__ = "agencias_inmobiliarias"

    nombre: Mapped[str] = mapped_column(String(255), index=True)

    municipio_oficina: Mapped[Optional["Municipio"]] = relationship(
        "Municipio",
        primaryjoin="foreign(AgenciaInmobiliaria.municipio_id) == Municipio.id",
        back_populates="agencias_inmobiliarias",
    )

    transmisiones_anunciadas: Mapped[list["TransmisionAnunciante"]] = relationship(
        "TransmisionAnunciante",
        back_populates="agencia_inmobiliaria",
    )

    def __repr__(self) -> str:
        return f"<AgenciaInmobiliaria {self.nombre}>"
