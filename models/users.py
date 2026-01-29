from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    Table,
    Column,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.registry import Base, metadata
from mixins import UUIDPKMixin, AuditMixin, IdentificacionMixin, ContactoMixin


# Tabla de asociación muchos-a-muchos
usuario_rol = Table(
    "usuario_rol",
    metadata,  # ← metadata del registry, no Base.metadata
    Column("usuario_id", String(36), ForeignKey("usuarios.id"), primary_key=True),
    Column("rol_id", String(36), ForeignKey("roles.id"), primary_key=True),
    Column(
        "fecha_asignacion",
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    ),
    Column(
        "asignado_por",
        String(36),
        ForeignKey("usuarios.id"),
        nullable=True,
    ),
)


class Usuario(UUIDPKMixin, AuditMixin, IdentificacionMixin, ContactoMixin, Base):
    __tablename__ = "usuarios"

    nombre_usuario: Mapped[str] = mapped_column(String(100))
    hashed_contrasena: Mapped[str] = mapped_column(Text)
    email_verificado: Mapped[bool] = mapped_column(Boolean, default=False)

    roles: Mapped[list["Rol"]] = relationship(
        "Rol",
        secondary=usuario_rol,
        back_populates="usuarios",
    )


class Rol(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "roles"

    nombre: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    usuarios: Mapped[list["Usuario"]] = relationship(
        "Usuario",
        secondary=usuario_rol,
        back_populates="roles",
    )
