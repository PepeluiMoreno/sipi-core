from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry

from db.registry import Base
from mixins import UUIDPKMixin, AuditMixin

class OSMPlace(UUIDPKMixin, AuditMixin, Base):
    """
    Censo local de lugares extraídos de OpenStreetMap.
    Se usa como referencia estática para geolocalización y matching.
    """
    __tablename__ = "osm_places"
    
    # ID original de OSM (ej: 'node/12345')
    osm_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    
    # Datos descriptivos
    name: Mapped[str] = mapped_column(String(255), index=True)
    amenity: Mapped[Optional[str]] = mapped_column(String(100), index=True) # place_of_worship, etc.
    religion: Mapped[Optional[str]] = mapped_column(String(50))
    denomination: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Ubicación normalizada
    municipio_id: Mapped[Optional[str]] = mapped_column(String(36), index=True) # Link to our Municipio if mapped
    addr_city: Mapped[Optional[str]] = mapped_column(String(100))
    addr_postcode: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Geometría (Punto)
    geom: Mapped[Geometry] = mapped_column(Geometry(geometry_type='POINT', srid=4326))
    
    # Raw tags para info extra
    tags: Mapped[Optional[dict]] = mapped_column(JSONB)
