from __future__ import annotations
from datetime import datetime
from typing import Optional
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, TIMESTAMP, Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB

from sipi.db.base import Base
from sipi.db.mixins import UUIDPKMixin, AuditMixin

class LifecycleEventType(str, Enum):
    # Fases principales
    ALTA_INMATRICULACION = "alta_inmatriculacion"
    PUESTA_EN_VENTA = "puesta_en_venta"
    VENDIDO = "vendido"
    CAMBIO_DE_USO = "cambio_de_uso"
    
    # Eventos de intervención
    REHABILITACION = "rehabilitacion"
    REHABILITACION_SUBVENCIONADA = "rehabilitacion_subvencionada"
    
    # Eventos administrativos
    DECLARACION_BIC = "declaracion_bic"
    CAMBIO_VISITABILIDAD = "cambio_visitabilidad"

class InmuebleLifecycle(UUIDPKMixin, AuditMixin, Base):
    """
    Historial de eventos en el ciclo de vida de un inmueble.
    Traza la evolución legal, física y de uso.
    """
    __tablename__ = "inmueble_lifecycle"
    
    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"), index=True)
    
    event_type: Mapped[LifecycleEventType] = mapped_column(SAEnum(LifecycleEventType), index=True)
    event_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, index=True)
    
    # Datos del cambio (ej: Precio de venta, NIF subvención, Nuevo Uso)
    details: Mapped[Optional[dict]] = mapped_column(JSONB)
    
    # Observaciones o descripción humana
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Origen del evento (Manual, Scraper-Idealista, Scraper-BOE)
    source: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Relación
    inmueble: Mapped["Inmueble"] = relationship("Inmueble", back_populates="lifecycle_events")
