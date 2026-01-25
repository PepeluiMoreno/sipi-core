from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Numeric, Boolean, ForeignKey
from geoalchemy2 import Geometry

from sipi.db.base import Base
from sipi.db.mixins import UUIDPKMixin, AuditMixin


class Inmueble(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles"
    
    nombre: Mapped[str] = mapped_column(String(255), index=True)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    # --- Visitabilidad ---
    es_visitable: Mapped[bool] = mapped_column(Boolean, default=False)
    horario_visitas: Mapped[Optional[str]] = mapped_column(Text)  # Obligatorio si BIC + Visitable
    enlace_web_visitas: Mapped[Optional[str]] = mapped_column(String(500))

    # --- Uso Religioso --- (deprecado: ahora se usa InmuebleUso)

    # --- Dependencias Complementarias (Auto-relación) ---
    inmueble_principal_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("inmuebles.id"), index=True)

    comunidad_autonoma_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("comunidades_autonomas.id"), index=True)
    provincia_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("provincias.id"), index=True)
    municipio_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("municipios.id"), index=True)
    direccion: Mapped[Optional[str]] = mapped_column(String(500))
    coordenadas: Mapped[Optional[Geometry]] = mapped_column(Geometry(geometry_type='POINT', srid=4326))
    
    tipo_inmueble_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("tipos_inmueble.id"), index=True)
    # figura_proteccion_id: Deprecado - usar InmuebleNivelProteccion
    estado_conservacion_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("estados_conservacion.id"), index=True)
    estado_tratamiento_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("estados_tratamiento.id"), index=True)

    # --- Relaciones Eclesiásticas ---
    diocesis_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("diocesis.id"), index=True)  # Demarcación geográfica
    entidad_religiosa_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("entidades_religiosas.id"), index=True)  # Gestor/Custodio

    # --- Propietario actual (polimórfico) ---
    propietario_tipo_actor: Mapped[Optional[str]] = mapped_column(String(50), index=True)  # Código TipoActor
    propietario_actor_id: Mapped[Optional[str]] = mapped_column(String(36), index=True)  # UUID del actor

    # --- Usufructuario actual (polimórfico) ---
    usufructuario_tipo_actor: Mapped[Optional[str]] = mapped_column(String(50), index=True)  # Código TipoActor
    usufructuario_actor_id: Mapped[Optional[str]] = mapped_column(String(36), index=True)  # UUID del actor
    
    superficie_construida: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    superficie_parcela: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    num_plantas: Mapped[Optional[int]]
    ano_construccion: Mapped[Optional[int]]
    
    valor_catastral: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2))
    valor_mercado: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2))
    
    en_venta: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    
    # Relaciones
    # Auto-relación para dependencias complementarias
    inmueble_principal: Mapped[Optional["Inmueble"]] = relationship(
        "Inmueble",
        remote_side="Inmueble.id",
        foreign_keys=[inmueble_principal_id],
        back_populates="dependencias_complementarias"
    )
    dependencias_complementarias: Mapped[List["Inmueble"]] = relationship(
        "Inmueble",
        foreign_keys="Inmueble.inmueble_principal_id",
        back_populates="inmueble_principal",
        cascade="all, delete-orphan"
    )

    # Relaciones geográficas
    comunidad_autonoma: Mapped[Optional["ComunidadAutonoma"]] = relationship("ComunidadAutonoma", back_populates="inmuebles")
    provincia: Mapped[Optional["Provincia"]] = relationship("Provincia", back_populates="inmuebles")
    municipio: Mapped[Optional["Municipio"]] = relationship("Municipio", back_populates="inmuebles")

    # Relaciones tipológicas y de estado
    tipo_inmueble: Mapped[Optional["TipoInmueble"]] = relationship("TipoInmueble", back_populates="inmuebles")
    # figura_proteccion: Deprecado - usar niveles_proteccion
    estado_conservacion: Mapped[Optional["TipoEstadoConservacion"]] = relationship("TipoEstadoConservacion", back_populates="inmuebles")
    estado_tratamiento: Mapped[Optional["TipoEstadoTratamiento"]] = relationship("TipoEstadoTratamiento", back_populates="inmuebles")

    # Relaciones eclesiásticas (geográfica y funcional)
    diocesis: Mapped[Optional["Diocesis"]] = relationship("Diocesis", back_populates="inmuebles")
    entidad_religiosa: Mapped[Optional["EntidadReligiosa"]] = relationship("EntidadReligiosa", back_populates="inmuebles")

    # Relaciones agregadas
    denominaciones: Mapped[List["InmuebleDenominacion"]] = relationship("InmuebleDenominacion", back_populates="inmueble", cascade="all, delete-orphan")
    inmatriculaciones: Mapped[List["Inmatriculacion"]] = relationship("Inmatriculacion", back_populates="inmueble", cascade="all, delete-orphan")
    osm_ext: Mapped[List["InmuebleOSMExt"]] = relationship("InmuebleOSMExt", back_populates="inmueble", cascade="all, delete-orphan")
    wd_ext: Mapped[List["InmuebleWDExt"]] = relationship("InmuebleWDExt", back_populates="inmueble", cascade="all, delete-orphan")
    citas: Mapped[List["InmuebleCita"]] = relationship("InmuebleCita", back_populates="inmueble", cascade="all, delete-orphan")

    # Documentos
    documentos: Mapped[List["InmuebleDocumento"]] = relationship("InmuebleDocumento", back_populates="inmueble", cascade="all, delete-orphan")

    # Transmisiones e intervenciones
    transmisiones: Mapped[List["Transmision"]] = relationship("Transmision", back_populates="inmueble", foreign_keys="[Transmision.inmueble_id]", cascade="all, delete-orphan")
    intervenciones: Mapped[List["Intervencion"]] = relationship("Intervencion", back_populates="inmueble", cascade="all, delete-orphan")

    # Usos del inmueble a lo largo del tiempo
    usos: Mapped[List["InmuebleUso"]] = relationship("InmuebleUso", back_populates="inmueble", cascade="all, delete-orphan")

    # Niveles de protección a lo largo del tiempo
    niveles_proteccion: Mapped[List["InmuebleNivelProteccion"]] = relationship("InmuebleNivelProteccion", back_populates="inmueble", cascade="all, delete-orphan")

    # Historial del inmueble (deprecado - los eventos ahora son tablas específicas)
    # - Inmatriculación → inmatriculaciones
    # - Enajenación → transmisiones
    # - Intervención arquitectónica → intervenciones
    # - Cambio de uso → inmuebles_usos
    # historial: Mapped[List["InmuebleEvento"]] = relationship("InmuebleEvento", back_populates="inmueble", cascade="all, delete-orphan")

    # Propiedades computadas
    @property
    def geo_quality_inferido(self) -> str:
        """Calcula la calidad de las coordenadas: MISSING, AUTO, MANUAL"""
        if self.coordenadas is None:
            return "MISSING"
        # TODO: implementar lógica para distinguir AUTO vs MANUAL
        # Por ahora retornar AUTO por defecto
        return "AUTO"

    @property
    def uso_religioso_activo(self) -> bool:
        """
        Indica si el inmueble tiene uso religioso activo actualmente.

        Retorna True si el uso actual (fecha_hasta=NULL) es de tipo "religioso"
        """
        for uso in self.usos:
            if uso.fecha_hasta is None:  # Uso actual
                if uso.tipo_uso and uso.tipo_uso.codigo == "religioso":
                    return True
        return False

    @property
    def figura_proteccion_actual(self) -> Optional[str]:
        """
        Retorna el ID de la figura de protección actual del inmueble.

        Consulta el historial de niveles de protección y retorna el ID
        de la figura activa (fecha_hasta=NULL).
        """
        for nivel in self.niveles_proteccion:
            if nivel.fecha_hasta is None:  # Nivel de protección actual
                return nivel.figura_proteccion_id
        return None

    @property
    def timeline_procesos(self) -> List[dict]:
        """
        Retorna todos los procesos del inmueble ordenados cronológicamente.

        Incluye: Inmatriculaciones, Transmisiones e Intervenciones.
        Cada entrada contiene: tipo, fecha, id, y datos relevantes del proceso.

        Returns:
            List[dict]: Lista de eventos ordenados por fecha (más reciente primero)
        """
        from datetime import datetime as dt

        eventos = []

        # Inmatriculaciones
        for inmat in self.inmatriculaciones:
            eventos.append({
                'tipo': 'INMATRICULACION',
                'fecha': inmat.fecha_inmatriculacion,
                'id': inmat.id,
                'numero_finca': inmat.numero_finca,
                'registro_propiedad_id': inmat.registro_propiedad_id,
                'tipo_certificacion_propiedad_id': inmat.tipo_certificacion_propiedad_id,
                'created_at': inmat.created_at,
            })

        # Transmisiones
        for trans in self.transmisiones:
            eventos.append({
                'tipo': 'TRANSMISION',
                'fecha': trans.fecha_transmision,
                'id': trans.id,
                'tipo_transmision_id': trans.tipo_transmision_id,
                'notaria_id': trans.notaria_id,
                'registro_propiedad_id': trans.registro_propiedad_id,
                'precio_venta': trans.precio_venta,
                'created_at': trans.created_at,
            })

        # Intervenciones
        for interv in self.intervenciones:
            eventos.append({
                'tipo': 'INTERVENCION',
                'fecha': interv.fecha_inicio,
                'fecha_fin': interv.fecha_fin,
                'id': interv.id,
                'nombre': interv.nombre,
                'descripcion': interv.descripcion,
                'presupuesto': interv.presupuesto,
                'created_at': interv.created_at,
            })

        # Ordenar por fecha (más reciente primero), usar created_at si fecha es None
        return sorted(
            eventos,
            key=lambda x: x['fecha'] or x['created_at'] or dt.min,
            reverse=True
        )


class Inmatriculacion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmatriculaciones"

    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"), index=True)
    registro_propiedad_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("registros_propiedad.id"), index=True)
    tipo_certificacion_propiedad_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("tipos_certificacion_propiedad.id"), index=True)

    fecha_inmatriculacion: Mapped[Optional[datetime]]
    numero_finca: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    tomo: Mapped[Optional[str]] = mapped_column(String(50))
    libro: Mapped[Optional[str]] = mapped_column(String(50))
    folio: Mapped[Optional[str]] = mapped_column(String(50))
    inscripcion: Mapped[Optional[str]] = mapped_column(String(50))
    tiene_dependencias: Mapped[bool] = mapped_column(Boolean, default=False)
    observaciones: Mapped[Optional[str]] = mapped_column(Text)
    
    inmueble: Mapped["Inmueble"] = relationship("Inmueble", back_populates="inmatriculaciones")
    registro_propiedad: Mapped[Optional["RegistroPropiedad"]] = relationship("RegistroPropiedad", back_populates="inmatriculaciones")
    tipo_certificacion_propiedad: Mapped[Optional["TipoCertificacionPropiedad"]] = relationship("TipoCertificacionPropiedad", back_populates="inmatriculaciones")


class InmuebleDenominacion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles_denominaciones"
    
    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"), index=True)
    denominacion: Mapped[str] = mapped_column(String(255), index=True)
    es_principal: Mapped[bool] = mapped_column(Boolean, default=False)
    
    inmueble: Mapped["Inmueble"] = relationship("Inmueble", back_populates="denominaciones")


class InmuebleOSMExt(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles_osm_ext"
    
    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"), index=True)
    osm_type: Mapped[str] = mapped_column(String(10))
    osm_id: Mapped[str] = mapped_column(String(50), index=True)
    osm_tags: Mapped[Optional[str]] = mapped_column(Text)
    
    inmueble: Mapped["Inmueble"] = relationship("Inmueble", back_populates="osm_ext")


class InmuebleWDExt(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles_wd_ext"
    
    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"), index=True)
    wikidata_qid: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    wikipedia_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    inmueble: Mapped["Inmueble"] = relationship("Inmueble", back_populates="wd_ext")


class InmuebleCita(UUIDPKMixin, AuditMixin, Base):
    """Cita bibliografica de un inmueble en una fuente"""
    __tablename__ = "citas_bibliograficas"

    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"), index=True)
    fuente_id: Mapped[str] = mapped_column(String(36), ForeignKey("fuentes_historiograficas.id"), index=True)
    referencia: Mapped[str] = mapped_column(String(500))
    pagina: Mapped[Optional[str]] = mapped_column(String(50))
    fecha: Mapped[Optional[datetime]]

    inmueble: Mapped["Inmueble"] = relationship("Inmueble", back_populates="citas")
    fuente: Mapped["FuenteHistoriografica"] = relationship("FuenteHistoriografica", back_populates="citas_bibliograficas")


class InmuebleUso(UUIDPKMixin, AuditMixin, Base):
    """
    Historial de usos del inmueble a lo largo del tiempo.

    Permite registrar los diferentes usos que ha tenido el inmueble
    con fechas de inicio y fin de cada uso.
    """
    __tablename__ = "inmuebles_usos"

    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"), index=True)
    tipo_uso_id: Mapped[str] = mapped_column(String(36), ForeignKey("tipos_uso_inmueble.id"), index=True)

    fecha_desde: Mapped[datetime] = mapped_column(index=True)
    fecha_hasta: Mapped[Optional[datetime]] = mapped_column(index=True)  # NULL = uso actual

    observaciones: Mapped[Optional[str]] = mapped_column(Text)

    # Relaciones
    inmueble: Mapped["Inmueble"] = relationship("Inmueble", back_populates="usos")
    tipo_uso: Mapped["TipoUsoInmueble"] = relationship("TipoUsoInmueble", back_populates="usos_inmuebles")


class InmuebleNivelProteccion(UUIDPKMixin, AuditMixin, Base):
    """
    Historial de niveles de protección del inmueble a lo largo del tiempo.

    Permite registrar los diferentes niveles de protección que ha tenido el inmueble
    con fechas de inicio y fin de cada nivel.
    """
    __tablename__ = "inmuebles_niveles_proteccion"

    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"), index=True)
    figura_proteccion_id: Mapped[str] = mapped_column(String(36), ForeignKey("tipos_figura_proteccion.id"), index=True)

    fecha_desde: Mapped[datetime] = mapped_column(index=True)
    fecha_hasta: Mapped[Optional[datetime]] = mapped_column(index=True)  # NULL = protección actual

    observaciones: Mapped[Optional[str]] = mapped_column(Text)

    # Relaciones
    inmueble: Mapped["Inmueble"] = relationship("Inmueble", back_populates="niveles_proteccion")
    figura_proteccion: Mapped["FiguraProteccion"] = relationship("FiguraProteccion")


# ============================================================================
# DEPRECADO: InmuebleEvento
# ============================================================================
# Los eventos ahora se representan mediante tablas específicas:
# - Inmatriculación → tabla inmatriculaciones
# - Enajenación → tabla transmisiones
# - Intervención arquitectónica → tabla intervenciones
# - Cambio de uso → tabla inmuebles_usos
#
# class InmuebleEvento(UUIDPKMixin, AuditMixin, Base):
#     """
#     Historial del inmueble: eventos detectados automáticamente.
#     DEPRECADO: Usar tablas específicas para cada tipo de evento.
#     """
#     __tablename__ = "inmuebles_eventos"
#
#     inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"), index=True)
#     tipo_evento_id: Mapped[str] = mapped_column(String(36), ForeignKey("eventos_registrables.id"), index=True)
#     fecha_evento: Mapped[datetime]
#     detalles: Mapped[Optional[dict]] = mapped_column(JSONB)
#     descripcion: Mapped[Optional[str]] = mapped_column(Text)
#     fuente: Mapped[Optional[str]] = mapped_column(String(50))
#
#     inmueble: Mapped["Inmueble"] = relationship("Inmueble", back_populates="historial")
#     tipo_evento: Mapped["EventoRegistrable"] = relationship("EventoRegistrable", back_populates="eventos")