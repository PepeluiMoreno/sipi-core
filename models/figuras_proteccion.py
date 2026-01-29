# models/figuras_proteccion.py
from __future__ import annotations
import enum
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey, Index, CheckConstraint, Enum as SQLEnum
import strawberry

from db.registry import Base
from mixins import UUIDPKMixin, AuditMixin

if TYPE_CHECKING:
    from models.gis import ComunidadAutonoma

@strawberry.enum
class NivelProteccion(str, enum.Enum):
    NACIONAL = "nacional"
    AUTONOMICO = "autonomico"
    LOCAL = "local"


class FiguraProteccion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_figura_proteccion"

    codigo: Mapped[str] = mapped_column(
        String(20),
        index=True,
        nullable=False,
        comment="Código identificador de la figura (BIC, BRL, BCIL, etc.)"
    )
    denominacion: Mapped[str] = mapped_column(
        String(255),
        index=True,
        nullable=False,
        comment="Denominación oficial corta"
    )
    denominacion_completa: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment="Denominación oficial completa"
    )
    descripcion: Mapped[Optional[str]] = mapped_column(
        Text,
        comment="Descripción de la figura de protección"
    )
    nivel: Mapped[NivelProteccion] = mapped_column(
        SQLEnum(
            NivelProteccion,
            name='nivel_proteccion',
            values_callable=lambda x: [e.value for e in x]
        ),
        index=True,
        nullable=False,
        comment="Nivel de protección: nacional, autonomico o local"
    )
    orden: Mapped[int] = mapped_column(
        Integer,
        default=999,
        nullable=False,
        comment="Orden de prioridad para ordenar listados (1=más importante)"
    )
    normativa: Mapped[Optional[str]] = mapped_column(Text, comment="Normativa legal que regula esta figura")
    url_normativa: Mapped[Optional[str]] = mapped_column(String(500), comment="URL a la ley o normativa reguladora")
    activo: Mapped[bool] = mapped_column(Boolean, default=True, index=True, nullable=False)

    comunidad_autonoma_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("comunidades_autonomas.id"),
        index=True,
        nullable=True,
        comment="NULL = figura de ámbito nacional. Con valor = figura autonómica específica"
    )

    comunidad_autonoma: Mapped[Optional["ComunidadAutonoma"]] = relationship(
        "ComunidadAutonoma",
        back_populates="figuras_proteccion"
    )

    __table_args__ = (
        CheckConstraint("(nivel != 'nacional') OR (comunidad_autonoma_id IS NULL)", name="ck_nacional_sin_ccaa"),
        CheckConstraint("(nivel != 'autonomico') OR (comunidad_autonoma_id IS NOT NULL)", name="ck_autonomico_con_ccaa"),
        Index('uq_codigo_ccaa', 'codigo', 'comunidad_autonoma_id', unique=True),
        Index('ix_figura_nivel', 'nivel'),
        Index('ix_figura_activo', 'activo'),
    )

    @property
    def es_nacional(self) -> bool:
        return self.nivel == NivelProteccion.NACIONAL

    @property
    def es_autonomica(self) -> bool:
        return self.nivel == NivelProteccion.AUTONOMICO

    @property
    def es_local(self) -> bool:
        return self.nivel == NivelProteccion.LOCAL

    @property
    def ambito(self) -> str:
        if self.es_nacional:
            return "Nacional (todas las CCAA)"
        elif self.comunidad_autonoma:
            return self.comunidad_autonoma.nombre
        return "Local/Municipal"

    @property
    def denominacion_con_ambito(self) -> str:
        if self.es_nacional:
            return f"{self.denominacion} (Nacional)"
        elif self.comunidad_autonoma:
            return f"{self.denominacion} ({self.comunidad_autonoma.codigo})"
        return self.denominacion

    @property
    def codigo_completo(self) -> str:
        if self.comunidad_autonoma:
            return f"{self.codigo}_{self.comunidad_autonoma.codigo}"
        return self.codigo

    def __repr__(self) -> str:
        return f"<TipoFiguraProteccion {self.codigo} - {self.denominacion} ({self.nivel})>"
