# app/db/mixins/base.py
from datetime import datetime, timezone
import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    declared_attr,
)
from sqlalchemy.schema import ForeignKey

if TYPE_CHECKING:
    from sipi.db.models.users import Usuario


UTCNOW = lambda: datetime.now(timezone.utc)


class UUIDPKMixin:
    """Clave primaria UUID estándar"""

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )


class AuditMixin:
    """Auditoría de creación, modificación y borrado lógico"""

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=UTCNOW,
        nullable=False,
        index=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=UTCNOW,
        onupdate=UTCNOW,
        nullable=False,
        index=True,
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        index=True,
    )

    # --- Usuarios responsables ---

    @declared_attr
    def created_by_id(cls) -> Mapped[Optional[str]]:
        return mapped_column(
            String(36),
            ForeignKey("usuarios.id"),
            nullable=True,
            index=True,
        )

    @declared_attr
    def updated_by_id(cls) -> Mapped[Optional[str]]:
        return mapped_column(
            String(36),
            ForeignKey("usuarios.id"),
            nullable=True,
            index=True,
        )

    @declared_attr
    def deleted_by_id(cls) -> Mapped[Optional[str]]:
        return mapped_column(
            String(36),
            ForeignKey("usuarios.id"),
            nullable=True,
            index=True,
        )

    # --- Relaciones (solo lectura) ---

    @declared_attr
    def created_by(cls) -> Mapped[Optional["Usuario"]]:
        return relationship(
            "Usuario",
            foreign_keys=[cls.created_by_id],
            viewonly=True,
        )

    @declared_attr
    def updated_by(cls) -> Mapped[Optional["Usuario"]]:
        return relationship(
            "Usuario",
            foreign_keys=[cls.updated_by_id],
            viewonly=True,
        )

    @declared_attr
    def deleted_by(cls) -> Mapped[Optional["Usuario"]]:
        return relationship(
            "Usuario",
            foreign_keys=[cls.deleted_by_id],
            viewonly=True,
        )

    # --- Comportamiento ---

    def soft_delete(self, user_id: Optional[str] = None) -> None:
        if self.is_deleted:
            return

        now = UTCNOW()
        self.is_deleted = True
        self.deleted_at = now
        self.updated_at = now

        if user_id:
            self.deleted_by_id = user_id
            self.updated_by_id = user_id

    def restore(self, user_id: Optional[str] = None) -> None:
        if not self.is_deleted:
            return

        now = UTCNOW()
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by_id = None
        self.updated_at = now

        if user_id:
            self.updated_by_id = user_id
