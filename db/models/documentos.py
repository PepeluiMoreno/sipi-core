# models/documentos.py
from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from .base import Base
from .mixins import UUIDPKMixin, AuditMixin, DocumentoMixin

class Documento(UUIDPKMixin, AuditMixin, DocumentoMixin, Base):
    __tablename__ = "documentos"
    tipo_documento_id: Mapped[str] = mapped_column(String(36), ForeignKey("tipos_documento.id", ondelete="RESTRICT"), index=True)
    tipo_licencia_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("tipos_licencia.id", ondelete="RESTRICT"), index=True)
    fuente_documental_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("fuentes_documentales.id", ondelete="RESTRICT"), index=True)

    # Relaciones
    inmuebles: Mapped[list["InmuebleDocumento"]] = relationship("InmuebleDocumento", back_populates="documento", cascade="all, delete-orphan")
    tipo_documento: Mapped["TipoDocumento"] = relationship("TipoDocumento", back_populates="documentos")
    tipo_licencia: Mapped[Optional["TipoLicencia"]] = relationship("TipoLicencia", back_populates="documentos")
    fuente_documental: Mapped[Optional["FuenteDocumental"]] = relationship("FuenteDocumental", back_populates="documentos")

class InmuebleDocumento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles_documentos"
    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id", ondelete="CASCADE"), index=True)
    documento_id: Mapped[str] = mapped_column(String(36), ForeignKey("documentos.id", ondelete="CASCADE"), index=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    inmueble: Mapped["Inmueble"] = relationship("Inmueble", back_populates="documentos")
    documento: Mapped["Documento"] = relationship("Documento", back_populates="inmuebles")

