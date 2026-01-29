
# models/discovery.py
from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    Text,
    Numeric,
    Boolean,
    ForeignKey,
    Integer,
    DateTime,
)
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry

from db.registry import Base
from mixins import AuditMixin

if TYPE_CHECKING:
    from models.inmuebles import Inmueble


class InmuebleRaw(Base, AuditMixin):
    __tablename__ = "portals_inmuebles_raw"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    portal: Mapped[str] = mapped_column(String(50))
    id_portal: Mapped[str] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(Text)

    titulo: Mapped[Optional[str]] = mapped_column(Text)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    tipo: Mapped[Optional[str]] = mapped_column(String(100))

    precio: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    superficie: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))

    geo_type: Mapped[str] = mapped_column(String(20))
    lat: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 7))
    lon: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 7))
    geom: Mapped[Optional[Geometry]] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326)
    )

    direccion: Mapped[Optional[str]] = mapped_column(Text)
    ciudad: Mapped[Optional[str]] = mapped_column(String(200))
    provincia: Mapped[Optional[str]] = mapped_column(String(200))

    scraped_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    detecciones: Mapped[List["DeteccionAnuncio"]] = relationship(
        "DeteccionAnuncio",
        back_populates="inmueble_raw",
        cascade="all, delete-orphan",
    )


class DeteccionAnuncio(Base, AuditMixin):
    __tablename__ = "portals_detecciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inmueble_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("portals_inmuebles_raw.id"),
        index=True,
    )

    inmueble_core_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("inmuebles.id"),
        index=True,
    )

    score: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    status: Mapped[str] = mapped_column(String(50))
    evidences: Mapped[Optional[dict]] = mapped_column(JSONB)

    first_detected_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    last_updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    inmueble_raw: Mapped["InmuebleRaw"] = relationship(
        "InmuebleRaw",
        back_populates="detecciones",
    )
    inmueble_core: Mapped[Optional["Inmueble"]] = relationship("Inmueble")
