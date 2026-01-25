"""initial_migration

Revision ID: e8a4ac3a0dc4
Revises:
Create Date: 2026-01-25 07:07:26.480641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision: str = 'e8a4ac3a0dc4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Schema único
SCHEMA = 'sipi'


def upgrade() -> None:
    # =========================================================================
    # 1. CREAR SCHEMA
    # =========================================================================
    op.execute(f'CREATE SCHEMA IF NOT EXISTS {SCHEMA}')

    # =========================================================================
    # 2. HABILITAR EXTENSIONES
    # =========================================================================
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis')
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # =========================================================================
    # 3. CREAR ENUMS
    # =========================================================================
    op.execute(f"CREATE TYPE {SCHEMA}.tipoidentificacion AS ENUM ('dni', 'nie', 'nif', 'cif', 'pasaporte', 'cif_extranjero', 'otro')")
    op.execute(f"CREATE TYPE {SCHEMA}.nivel_proteccion AS ENUM ('nacional', 'autonomico', 'local')")

    # =========================================================================
    # 4. TABLAS BASE (SIN FKs o con FKs a sí mismas)
    # =========================================================================

    # --- usuarios (base para AuditMixin) ---
    op.create_table('usuarios',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, index=True),
        sa.Column('updated_at', sa.DateTime(), index=True),
        sa.Column('deleted_at', sa.DateTime(), index=True),
        sa.Column('created_by_id', sa.String(36), index=True),
        sa.Column('updated_by_id', sa.String(36), index=True),
        sa.Column('deleted_by_id', sa.String(36), index=True),
        sa.Column('created_from_ip', sa.String(45)),
        sa.Column('updated_from_ip', sa.String(45)),
        # IdentificacionMixin
        sa.Column('tipo_identificacion', sa.Enum('dni', 'nie', 'nif', 'cif', 'pasaporte', 'cif_extranjero', 'otro', name='tipoidentificacion', schema=SCHEMA), index=True),
        sa.Column('identificacion', sa.String(50), index=True),
        sa.Column('nombre', sa.String(255), nullable=False),
        sa.Column('apellidos', sa.String(200)),
        sa.Column('identificacion_extranjera', sa.String(50)),
        # ContactoMixin
        sa.Column('email_personal', sa.String(255), index=True),
        sa.Column('email_corporativo', sa.String(255), index=True),
        sa.Column('telefono', sa.String(20)),
        sa.Column('telefono_movil', sa.String(20)),
        sa.Column('fax', sa.String(20)),
        sa.Column('sitio_web', sa.String(500)),
        sa.Column('notas', sa.String(500)),
        # Campos específicos de Usuario
        sa.Column('nombre_usuario', sa.String(100), nullable=False),
        sa.Column('hashed_contrasena', sa.Text(), nullable=False),
        sa.Column('email_verificado', sa.Boolean(), default=False),
        schema=SCHEMA
    )

    # Self-referential FKs para usuarios (AuditMixin)
    op.create_foreign_key('fk_usuarios_created_by', 'usuarios', 'usuarios', ['created_by_id'], ['id'], source_schema=SCHEMA, referent_schema=SCHEMA)
    op.create_foreign_key('fk_usuarios_updated_by', 'usuarios', 'usuarios', ['updated_by_id'], ['id'], source_schema=SCHEMA, referent_schema=SCHEMA)
    op.create_foreign_key('fk_usuarios_deleted_by', 'usuarios', 'usuarios', ['deleted_by_id'], ['id'], source_schema=SCHEMA, referent_schema=SCHEMA)

    # --- roles ---
    op.create_table('roles',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, index=True),
        sa.Column('updated_at', sa.DateTime(), index=True),
        sa.Column('deleted_at', sa.DateTime(), index=True),
        sa.Column('created_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('updated_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('deleted_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('created_from_ip', sa.String(45)),
        sa.Column('updated_from_ip', sa.String(45)),
        sa.Column('nombre', sa.String(50), unique=True, index=True, nullable=False),
        sa.Column('descripcion', sa.Text()),
        schema=SCHEMA
    )

    # --- usuario_rol (M2M) ---
    op.create_table('usuario_rol',
        sa.Column('usuario_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), primary_key=True),
        sa.Column('rol_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.roles.id'), primary_key=True),
        sa.Column('fecha_asignacion', sa.DateTime()),
        sa.Column('asignado_por', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id')),
        schema=SCHEMA
    )

    # =========================================================================
    # 5. TIPOLOGÍAS
    # =========================================================================

    def create_tipologia_table(tablename, extra_columns=None):
        columns = [
            sa.Column('id', sa.String(36), primary_key=True),
            sa.Column('created_at', sa.DateTime(), nullable=False, index=True),
            sa.Column('updated_at', sa.DateTime(), index=True),
            sa.Column('deleted_at', sa.DateTime(), index=True),
            sa.Column('created_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
            sa.Column('updated_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
            sa.Column('deleted_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
            sa.Column('created_from_ip', sa.String(45)),
            sa.Column('updated_from_ip', sa.String(45)),
            sa.Column('nombre', sa.String(100), unique=True, index=True, nullable=False),
            sa.Column('descripcion', sa.Text()),
        ]
        if extra_columns:
            columns.extend(extra_columns)
        op.create_table(tablename, *columns, schema=SCHEMA)

    create_tipologia_table('estados_conservacion')
    create_tipologia_table('estados_tratamiento')
    create_tipologia_table('roles_tecnico')
    create_tipologia_table('tipos_certificacion_propiedad')
    create_tipologia_table('tipos_documento')
    create_tipologia_table('tipos_inmueble')
    create_tipologia_table('tipos_persona')
    create_tipologia_table('tipos_transmision')
    create_tipologia_table('tipos_via')
    create_tipologia_table('tipos_entidad_religiosa')
    create_tipologia_table('tipos_uso_inmueble', [
        sa.Column('codigo', sa.String(50), unique=True, index=True, nullable=False),
        sa.Column('activo', sa.Boolean(), default=True, nullable=False, index=True),
    ])

    op.create_table('tipos_titulo_propiedad',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, index=True),
        sa.Column('updated_at', sa.DateTime(), index=True),
        sa.Column('deleted_at', sa.DateTime(), index=True),
        sa.Column('created_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('updated_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('deleted_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('created_from_ip', sa.String(45)),
        sa.Column('updated_from_ip', sa.String(45)),
        sa.Column('codigo', sa.String(50), unique=True, index=True, nullable=False),
        sa.Column('nombre', sa.String(200), nullable=False),
        sa.Column('descripcion', sa.Text()),
        sa.Column('activo', sa.Boolean(), default=True),
        schema=SCHEMA
    )

    op.create_table('tipos_mime_documento',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, index=True),
        sa.Column('updated_at', sa.DateTime(), index=True),
        sa.Column('deleted_at', sa.DateTime(), index=True),
        sa.Column('created_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('updated_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('deleted_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('created_from_ip', sa.String(45)),
        sa.Column('updated_from_ip', sa.String(45)),
        sa.Column('tipo_mime', sa.String(100), unique=True, index=True, nullable=False),
        sa.Column('extension', sa.String(10), nullable=False),
        sa.Column('descripcion', sa.Text()),
        schema=SCHEMA
    )

    op.create_table('tipos_licencia',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, index=True),
        sa.Column('updated_at', sa.DateTime(), index=True),
        sa.Column('deleted_at', sa.DateTime(), index=True),
        sa.Column('created_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('updated_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('deleted_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('created_from_ip', sa.String(45)),
        sa.Column('updated_from_ip', sa.String(45)),
        sa.Column('codigo', sa.String(50), unique=True, index=True, nullable=False),
        sa.Column('nombre', sa.String(200), nullable=False),
        sa.Column('nombre_corto', sa.String(100)),
        sa.Column('descripcion', sa.Text()),
        sa.Column('url_licencia', sa.String(500)),
        sa.Column('url_legal', sa.String(500)),
        sa.Column('requiere_atribucion', sa.Boolean(), default=False, nullable=False),
        sa.Column('permite_uso_comercial', sa.Boolean(), default=True, nullable=False),
        sa.Column('permite_derivadas', sa.Boolean(), default=True, nullable=False),
        sa.Column('requiere_compartir_igual', sa.Boolean(), default=False, nullable=False),
        sa.Column('es_libre', sa.Boolean(), default=True, nullable=False, index=True),
        sa.Column('es_open_source', sa.Boolean(), default=False, nullable=False),
        sa.Column('es_copyleft', sa.Boolean(), default=False, nullable=False),
        sa.Column('version', sa.String(20)),
        sa.Column('jurisdiccion', sa.String(50)),
        sa.Column('familia', sa.String(50), index=True),
        sa.Column('icono_url', sa.String(500)),
        sa.Column('color_hex', sa.String(7)),
        sa.Column('popularidad', sa.Integer(), default=0, nullable=False),
        sa.Column('recomendada', sa.Boolean(), default=False, nullable=False, index=True),
        sa.Column('obsoleta', sa.Boolean(), default=False, nullable=False, index=True),
        schema=SCHEMA
    )

    op.create_table('fuentes_documentales',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, index=True),
        sa.Column('updated_at', sa.DateTime(), index=True),
        sa.Column('deleted_at', sa.DateTime(), index=True),
        sa.Column('created_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('updated_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('deleted_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('created_from_ip', sa.String(45)),
        sa.Column('updated_from_ip', sa.String(45)),
        sa.Column('codigo', sa.String(50), unique=True, index=True, nullable=False),
        sa.Column('nombre', sa.String(200), nullable=False),
        sa.Column('descripcion', sa.Text()),
        sa.Column('url_fuente', sa.String(500)),
        sa.Column('es_externa', sa.Boolean(), default=False, nullable=False, index=True),
        sa.Column('requiere_url_externa', sa.Boolean(), default=False, nullable=False),
        sa.Column('permite_metadata_extra', sa.Boolean(), default=False, nullable=False),
        sa.Column('licencia_predeterminada_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.tipos_licencia.id')),
        sa.Column('categoria', sa.String(50), index=True),
        sa.Column('soporta_sincronizacion', sa.Boolean(), default=False, nullable=False),
        sa.Column('frecuencia_sync_dias', sa.Integer()),
        sa.Column('api_endpoint', sa.String(500)),
        sa.Column('requiere_autenticacion', sa.Boolean(), default=False, nullable=False),
        sa.Column('icono', sa.String(100)),
        sa.Column('color_hex', sa.String(7)),
        sa.Column('orden', sa.Integer(), default=0, nullable=False),
        sa.Column('activa', sa.Boolean(), default=True, nullable=False, index=True),
        schema=SCHEMA
    )

    # =========================================================================
    # 6. GEOGRAFÍA
    # =========================================================================

    op.create_table('comunidades_autonomas',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, index=True),
        sa.Column('updated_at', sa.DateTime(), index=True),
        sa.Column('deleted_at', sa.DateTime(), index=True),
        sa.Column('created_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('updated_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('deleted_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('created_from_ip', sa.String(45)),
        sa.Column('updated_from_ip', sa.String(45)),
        sa.Column('codigo_ine', sa.String(2), unique=True, index=True, nullable=False),
        sa.Column('nombre', sa.String(100), index=True, nullable=False),
        sa.Column('nombre_oficial', sa.String(150)),
        sa.Column('capital', sa.String(100)),
        sa.Column('activo', sa.Boolean(), default=True, index=True, nullable=False),
        schema=SCHEMA
    )

    op.create_table('provincias',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, index=True),
        sa.Column('updated_at', sa.DateTime(), index=True),
        sa.Column('deleted_at', sa.DateTime(), index=True),
        sa.Column('created_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('updated_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('deleted_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('created_from_ip', sa.String(45)),
        sa.Column('updated_from_ip', sa.String(45)),
        sa.Column('codigo_ine', sa.String(2), unique=True, index=True, nullable=False),
        sa.Column('nombre', sa.String(100), index=True, nullable=False),
        sa.Column('nombre_oficial', sa.String(150)),
        sa.Column('capital', sa.String(100)),
        sa.Column('comunidad_autonoma_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.comunidades_autonomas.id'), index=True, nullable=False),
        sa.Column('activo', sa.Boolean(), default=True, index=True, nullable=False),
        schema=SCHEMA
    )

    op.create_table('municipios',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, index=True),
        sa.Column('updated_at', sa.DateTime(), index=True),
        sa.Column('deleted_at', sa.DateTime(), index=True),
        sa.Column('created_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('updated_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('deleted_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('created_from_ip', sa.String(45)),
        sa.Column('updated_from_ip', sa.String(45)),
        sa.Column('codigo_ine', sa.String(5), unique=True, index=True),
        sa.Column('nombre', sa.String(150), index=True, nullable=False),
        sa.Column('nombre_oficial', sa.String(200)),
        sa.Column('provincia_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.provincias.id'), index=True, nullable=False),
        sa.Column('comunidad_autonoma_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.comunidades_autonomas.id'), index=True, nullable=False),
        sa.Column('activo', sa.Boolean(), default=True, index=True),
        schema=SCHEMA
    )

    op.create_table('tipos_figura_proteccion',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, index=True),
        sa.Column('updated_at', sa.DateTime(), index=True),
        sa.Column('deleted_at', sa.DateTime(), index=True),
        sa.Column('created_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('updated_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('deleted_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
        sa.Column('created_from_ip', sa.String(45)),
        sa.Column('updated_from_ip', sa.String(45)),
        sa.Column('codigo', sa.String(20), index=True, nullable=False),
        sa.Column('denominacion', sa.String(255), index=True, nullable=False),
        sa.Column('denominacion_completa', sa.String(500), nullable=False),
        sa.Column('descripcion', sa.Text()),
        sa.Column('nivel', sa.Enum('nacional', 'autonomico', 'local', name='nivel_proteccion', schema=SCHEMA), index=True, nullable=False),
        sa.Column('orden', sa.Integer(), default=999, nullable=False),
        sa.Column('normativa', sa.Text()),
        sa.Column('url_normativa', sa.String(500)),
        sa.Column('activo', sa.Boolean(), default=True, index=True, nullable=False),
        sa.Column('comunidad_autonoma_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.comunidades_autonomas.id'), index=True),
        sa.CheckConstraint("(nivel != 'nacional') OR (comunidad_autonoma_id IS NULL)", name='ck_nacional_sin_ccaa'),
        sa.CheckConstraint("(nivel != 'autonomico') OR (comunidad_autonoma_id IS NOT NULL)", name='ck_autonomico_con_ccaa'),
        sa.Index('uq_codigo_ccaa', 'codigo', 'comunidad_autonoma_id', unique=True),
        schema=SCHEMA
    )

    # =========================================================================
    # 7. ACTORES
    # =========================================================================

    def audit_columns():
        return [
            sa.Column('id', sa.String(36), primary_key=True),
            sa.Column('created_at', sa.DateTime(), nullable=False, index=True),
            sa.Column('updated_at', sa.DateTime(), index=True),
            sa.Column('deleted_at', sa.DateTime(), index=True),
            sa.Column('created_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
            sa.Column('updated_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
            sa.Column('deleted_by_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.usuarios.id'), index=True),
            sa.Column('created_from_ip', sa.String(45)),
            sa.Column('updated_from_ip', sa.String(45)),
        ]

    def identificacion_columns():
        return [
            sa.Column('tipo_identificacion', sa.Enum('dni', 'nie', 'nif', 'cif', 'pasaporte', 'cif_extranjero', 'otro', name='tipoidentificacion', schema=SCHEMA, create_type=False), index=True),
            sa.Column('identificacion', sa.String(50), index=True),
            sa.Column('nombre', sa.String(255), nullable=False),
            sa.Column('apellidos', sa.String(200)),
            sa.Column('identificacion_extranjera', sa.String(50)),
        ]

    def contacto_columns():
        return [
            sa.Column('email_personal', sa.String(255), index=True),
            sa.Column('email_corporativo', sa.String(255), index=True),
            sa.Column('telefono', sa.String(20)),
            sa.Column('telefono_movil', sa.String(20)),
            sa.Column('fax', sa.String(20)),
            sa.Column('sitio_web', sa.String(500)),
            sa.Column('notas', sa.String(500)),
        ]

    def direccion_columns():
        return [
            sa.Column('tipo_via_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.tipos_via.id'), index=True),
            sa.Column('nombre_via', sa.String(255)),
            sa.Column('numero', sa.String(10)),
            sa.Column('bloque', sa.String(10)),
            sa.Column('escalera', sa.String(10)),
            sa.Column('piso', sa.String(10)),
            sa.Column('puerta', sa.String(10)),
            sa.Column('codigo_postal', sa.String(10), index=True),
            sa.Column('comunidad_autonoma_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.comunidades_autonomas.id'), index=True),
            sa.Column('provincia_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.provincias.id'), index=True),
            sa.Column('municipio_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.municipios.id'), index=True),
            sa.Column('latitud', sa.Float(precision=10, asdecimal=True)),
            sa.Column('longitud', sa.Float(precision=10, asdecimal=True)),
        ]

    op.create_table('privados',
        *audit_columns(),
        sa.Column('tipo_identificacion', sa.Enum('dni', 'nie', 'nif', 'cif', 'pasaporte', 'cif_extranjero', 'otro', name='tipoidentificacion', schema=SCHEMA, create_type=False), index=True),
        sa.Column('identificacion', sa.String(50), index=True),
        sa.Column('nombre', sa.String(255), nullable=False),
        sa.Column('apellidos', sa.String(200)),
        sa.Column('identificacion_extranjera', sa.String(50)),
        sa.Column('tipo_persona_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.tipos_persona.id'), index=True),
        *contacto_columns(),
        *direccion_columns(),
        schema=SCHEMA
    )

    op.create_table('colegios_profesionales',
        *audit_columns(),
        *contacto_columns(),
        *direccion_columns(),
        sa.Column('nombre', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('codigo', sa.String(50), unique=True, index=True),
        schema=SCHEMA
    )

    op.create_table('tecnicos',
        *audit_columns(),
        *identificacion_columns(),
        *contacto_columns(),
        *direccion_columns(),
        sa.Column('rol_tecnico_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.roles_tecnico.id'), index=True),
        sa.Column('colegio_profesional_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.colegios_profesionales.id'), index=True),
        sa.Column('numero_colegiado', sa.String(50), index=True),
        sa.Column('fecha_colegiacion', sa.DateTime()),
        schema=SCHEMA
    )

    op.create_table('administraciones',
        *audit_columns(),
        *contacto_columns(),
        *direccion_columns(),
        sa.Column('nombre', sa.String(255), index=True, nullable=False),
        sa.Column('codigo_oficial', sa.String(100), unique=True, index=True),
        sa.Column('ambito', sa.String(100)),
        sa.Column('administracion_padre_id', sa.String(36), index=True),
        sa.Column('nivel_jerarquico', sa.String(50), index=True),
        sa.Column('tipo_organo', sa.String(100), index=True),
        sa.Column('orden_jerarquico', sa.Integer(), index=True),
        sa.Column('valido_desde', sa.DateTime(), index=True),
        sa.Column('valido_hasta', sa.DateTime(), index=True),
        sa.Column('activa', sa.Boolean(), default=True, index=True),
        schema=SCHEMA
    )
    op.create_foreign_key('fk_admin_padre', 'administraciones', 'administraciones', ['administracion_padre_id'], ['id'], source_schema=SCHEMA, referent_schema=SCHEMA)

    op.create_table('administraciones_titulares',
        *audit_columns(),
        *identificacion_columns(),
        *contacto_columns(),
        *direccion_columns(),
        sa.Column('fecha_inicio', sa.DateTime(), index=True, nullable=False),
        sa.Column('fecha_fin', sa.DateTime(), index=True),
        sa.Column('cargo', sa.String(100)),
        sa.Column('administracion_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.administraciones.id'), index=True, nullable=False),
        schema=SCHEMA
    )

    op.create_table('diocesis',
        *audit_columns(),
        *contacto_columns(),
        *direccion_columns(),
        sa.Column('nombre', sa.String(100), unique=True, index=True, nullable=False),
        sa.Column('wikidata_qid', sa.String(32), unique=True, index=True),
        schema=SCHEMA
    )

    op.create_table('diocesis_titulares',
        *audit_columns(),
        *identificacion_columns(),
        sa.Column('fecha_inicio', sa.DateTime(), index=True, nullable=False),
        sa.Column('fecha_fin', sa.DateTime(), index=True),
        sa.Column('cargo', sa.String(100)),
        sa.Column('diocesis_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.diocesis.id'), index=True, nullable=False),
        schema=SCHEMA
    )

    op.create_table('notarias',
        *audit_columns(),
        *contacto_columns(),
        *direccion_columns(),
        sa.Column('nombre', sa.String(255), index=True, nullable=False),
        schema=SCHEMA
    )

    op.create_table('notarias_titulares',
        *audit_columns(),
        *identificacion_columns(),
        sa.Column('fecha_inicio', sa.DateTime(), index=True, nullable=False),
        sa.Column('fecha_fin', sa.DateTime(), index=True),
        sa.Column('cargo', sa.String(100)),
        sa.Column('notaria_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.notarias.id'), index=True, nullable=False),
        schema=SCHEMA
    )

    op.create_table('registros_propiedad',
        *audit_columns(),
        *identificacion_columns(),
        *contacto_columns(),
        *direccion_columns(),
        schema=SCHEMA
    )

    op.create_table('registros_propiedad_titulares',
        *audit_columns(),
        *identificacion_columns(),
        sa.Column('fecha_inicio', sa.DateTime(), index=True, nullable=False),
        sa.Column('fecha_fin', sa.DateTime(), index=True),
        sa.Column('cargo', sa.String(100)),
        sa.Column('registro_propiedad_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.registros_propiedad.id'), index=True, nullable=False),
        schema=SCHEMA
    )

    op.create_table('entidades_religiosas',
        *audit_columns(),
        *identificacion_columns(),
        *contacto_columns(),
        *direccion_columns(),
        sa.Column('tipo_entidad_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.tipos_entidad_religiosa.id', ondelete='RESTRICT'), index=True),
        sa.Column('fecha_fundacion', sa.DateTime()),
        sa.Column('activa', sa.Boolean(), default=True),
        schema=SCHEMA
    )

    op.create_table('entidades_religiosas_titulares',
        *audit_columns(),
        *identificacion_columns(),
        sa.Column('fecha_inicio', sa.DateTime(), index=True, nullable=False),
        sa.Column('fecha_fin', sa.DateTime(), index=True),
        sa.Column('cargo', sa.String(100)),
        sa.Column('entidad_religiosa_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.entidades_religiosas.id', ondelete='CASCADE'), index=True, nullable=False),
        schema=SCHEMA
    )

    op.create_table('agencias_inmobiliarias',
        *audit_columns(),
        *contacto_columns(),
        *direccion_columns(),
        sa.Column('nombre', sa.String(255), index=True, nullable=False),
        schema=SCHEMA
    )

    # =========================================================================
    # 8. HISTORIOGRAFÍA
    # =========================================================================

    op.create_table('fuentes_historiograficas',
        *audit_columns(),
        sa.Column('nombre', sa.String(255), index=True, nullable=False),
        sa.Column('descripcion', sa.Text()),
        sa.Column('activo', sa.Boolean(), default=True, index=True),
        schema=SCHEMA
    )

    # =========================================================================
    # 9. INMUEBLES Y RELACIONADOS
    # =========================================================================

    op.create_table('inmuebles',
        *audit_columns(),
        sa.Column('nombre', sa.String(255), index=True, nullable=False),
        sa.Column('descripcion', sa.Text()),
        sa.Column('es_visitable', sa.Boolean(), default=False),
        sa.Column('horario_visitas', sa.Text()),
        sa.Column('enlace_web_visitas', sa.String(500)),
        sa.Column('inmueble_principal_id', sa.String(36), index=True),
        sa.Column('comunidad_autonoma_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.comunidades_autonomas.id'), index=True),
        sa.Column('provincia_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.provincias.id'), index=True),
        sa.Column('municipio_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.municipios.id'), index=True),
        sa.Column('direccion', sa.String(500)),
        sa.Column('coordenadas', Geometry(geometry_type='POINT', srid=4326)),
        sa.Column('tipo_inmueble_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.tipos_inmueble.id'), index=True),
        sa.Column('estado_conservacion_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.estados_conservacion.id'), index=True),
        sa.Column('estado_tratamiento_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.estados_tratamiento.id'), index=True),
        sa.Column('diocesis_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.diocesis.id'), index=True),
        sa.Column('entidad_religiosa_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.entidades_religiosas.id'), index=True),
        sa.Column('propietario_tipo_actor', sa.String(50), index=True),
        sa.Column('propietario_actor_id', sa.String(36), index=True),
        sa.Column('usufructuario_tipo_actor', sa.String(50), index=True),
        sa.Column('usufructuario_actor_id', sa.String(36), index=True),
        sa.Column('superficie_construida', sa.Numeric(10, 2)),
        sa.Column('superficie_parcela', sa.Numeric(10, 2)),
        sa.Column('num_plantas', sa.Integer()),
        sa.Column('ano_construccion', sa.Integer()),
        sa.Column('valor_catastral', sa.Numeric(15, 2)),
        sa.Column('valor_mercado', sa.Numeric(15, 2)),
        sa.Column('en_venta', sa.Boolean(), default=False, index=True),
        sa.Column('activo', sa.Boolean(), default=True, index=True),
        schema=SCHEMA
    )
    op.create_foreign_key('fk_inmueble_principal', 'inmuebles', 'inmuebles', ['inmueble_principal_id'], ['id'], source_schema=SCHEMA, referent_schema=SCHEMA)

    op.create_table('inmatriculaciones',
        *audit_columns(),
        sa.Column('inmueble_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.inmuebles.id'), index=True, nullable=False),
        sa.Column('registro_propiedad_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.registros_propiedad.id'), index=True),
        sa.Column('tipo_certificacion_propiedad_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.tipos_certificacion_propiedad.id'), index=True),
        sa.Column('fecha_inmatriculacion', sa.DateTime()),
        sa.Column('numero_finca', sa.String(50), index=True),
        sa.Column('tomo', sa.String(50)),
        sa.Column('libro', sa.String(50)),
        sa.Column('folio', sa.String(50)),
        sa.Column('inscripcion', sa.String(50)),
        sa.Column('tiene_dependencias', sa.Boolean(), default=False),
        sa.Column('observaciones', sa.Text()),
        schema=SCHEMA
    )

    op.create_table('inmuebles_denominaciones',
        *audit_columns(),
        sa.Column('inmueble_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.inmuebles.id'), index=True, nullable=False),
        sa.Column('denominacion', sa.String(255), index=True, nullable=False),
        sa.Column('es_principal', sa.Boolean(), default=False),
        schema=SCHEMA
    )

    op.create_table('inmuebles_osm_ext',
        *audit_columns(),
        sa.Column('inmueble_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.inmuebles.id'), index=True, nullable=False),
        sa.Column('osm_type', sa.String(10), nullable=False),
        sa.Column('osm_id', sa.String(50), index=True, nullable=False),
        sa.Column('osm_tags', sa.Text()),
        schema=SCHEMA
    )

    op.create_table('inmuebles_wd_ext',
        *audit_columns(),
        sa.Column('inmueble_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.inmuebles.id'), index=True, nullable=False),
        sa.Column('wikidata_qid', sa.String(32), unique=True, index=True, nullable=False),
        sa.Column('wikipedia_url', sa.String(500)),
        schema=SCHEMA
    )

    op.create_table('citas_bibliograficas',
        *audit_columns(),
        sa.Column('inmueble_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.inmuebles.id'), index=True, nullable=False),
        sa.Column('fuente_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.fuentes_historiograficas.id'), index=True, nullable=False),
        sa.Column('referencia', sa.String(500), nullable=False),
        sa.Column('pagina', sa.String(50)),
        sa.Column('fecha', sa.DateTime()),
        schema=SCHEMA
    )

    op.create_table('inmuebles_usos',
        *audit_columns(),
        sa.Column('inmueble_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.inmuebles.id'), index=True, nullable=False),
        sa.Column('tipo_uso_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.tipos_uso_inmueble.id'), index=True, nullable=False),
        sa.Column('fecha_desde', sa.DateTime(), index=True, nullable=False),
        sa.Column('fecha_hasta', sa.DateTime(), index=True),
        sa.Column('observaciones', sa.Text()),
        schema=SCHEMA
    )

    op.create_table('inmuebles_niveles_proteccion',
        *audit_columns(),
        sa.Column('inmueble_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.inmuebles.id'), index=True, nullable=False),
        sa.Column('figura_proteccion_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.tipos_figura_proteccion.id'), index=True, nullable=False),
        sa.Column('fecha_desde', sa.DateTime(), index=True, nullable=False),
        sa.Column('fecha_hasta', sa.DateTime(), index=True),
        sa.Column('observaciones', sa.Text()),
        schema=SCHEMA
    )

    # =========================================================================
    # 10. DOCUMENTOS
    # =========================================================================

    op.create_table('documentos',
        *audit_columns(),
        sa.Column('tipo_documento_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.tipos_documento.id', ondelete='RESTRICT'), index=True, nullable=False),
        sa.Column('tipo_licencia_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.tipos_licencia.id', ondelete='RESTRICT'), index=True),
        sa.Column('fuente_documental_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.fuentes_documentales.id', ondelete='RESTRICT'), index=True),
        sa.Column('nombre_archivo', sa.String(255)),
        sa.Column('tipo_mime', sa.String(100)),
        sa.Column('tamano_bytes', sa.Integer()),
        sa.Column('hash_sha256', sa.String(64)),
        sa.Column('origen', sa.String(50), index=True),
        sa.Column('origen_metadata', postgresql.JSONB()),
        sa.Column('descripcion', sa.Text()),
        sa.Column('fecha_documento', sa.DateTime()),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('url_valida', sa.Boolean()),
        sa.Column('url_ultimo_check', sa.DateTime()),
        sa.Column('storage_type', sa.String(50)),
        schema=SCHEMA
    )

    op.create_table('inmuebles_documentos',
        *audit_columns(),
        sa.Column('inmueble_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.inmuebles.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('documento_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.documentos.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('descripcion', sa.Text()),
        schema=SCHEMA
    )

    # =========================================================================
    # 11. TRANSMISIONES
    # =========================================================================

    op.create_table('transmisiones',
        *audit_columns(),
        sa.Column('inmueble_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.inmuebles.id'), index=True, nullable=False),
        sa.Column('notaria_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.notarias.id'), index=True),
        sa.Column('registro_propiedad_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.registros_propiedad.id'), index=True),
        sa.Column('tipo_transmision_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.tipos_transmision.id'), index=True),
        sa.Column('tipo_certificacion_propiedad_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.tipos_certificacion_propiedad.id'), index=True),
        sa.Column('fecha_transmision', sa.DateTime(), index=True),
        sa.Column('descripcion', sa.Text()),
        sa.Column('precio_venta', sa.Numeric(15, 2)),
        schema=SCHEMA
    )

    op.create_table('transmision_anunciantes',
        *audit_columns(),
        sa.Column('transmision_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.transmisiones.id'), index=True, nullable=False),
        sa.Column('agencia_inmobiliaria_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.agencias_inmobiliarias.id'), index=True, nullable=False),
        schema=SCHEMA
    )

    # =========================================================================
    # 12. INTERVENCIONES
    # =========================================================================

    op.create_table('intervenciones',
        *audit_columns(),
        sa.Column('inmueble_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.inmuebles.id'), index=True, nullable=False),
        sa.Column('nombre', sa.String(255), index=True, nullable=False),
        sa.Column('descripcion', sa.Text()),
        sa.Column('fecha_inicio', sa.DateTime(), index=True),
        sa.Column('fecha_fin', sa.DateTime(), index=True),
        sa.Column('presupuesto', sa.Numeric(15, 2)),
        schema=SCHEMA
    )

    op.create_table('intervenciones_tecnicos',
        *audit_columns(),
        sa.Column('intervencion_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.intervenciones.id'), index=True, nullable=False),
        sa.Column('tecnico_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.tecnicos.id'), index=True, nullable=False),
        sa.Column('rol_tecnico_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.roles_tecnico.id'), index=True, nullable=False),
        sa.Column('descripcion', sa.Text()),
        sa.Column('fecha_inicio', sa.DateTime(), index=True),
        sa.Column('fecha_fin', sa.DateTime(), index=True),
        schema=SCHEMA
    )

    # =========================================================================
    # 13. SUBVENCIONES
    # =========================================================================

    op.create_table('intervenciones_subvenciones',
        *audit_columns(),
        sa.Column('intervencion_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.intervenciones.id'), index=True, nullable=False),
        sa.Column('codigo_concesion', sa.String(100), index=True, nullable=False),
        sa.Column('importe_aplicado', sa.Numeric(15, 2)),
        sa.Column('porcentaje_financiacion', sa.Numeric(5, 2)),
        sa.Column('justificacion_gasto', sa.Text()),
        sa.Column('observaciones', sa.Text()),
        schema=SCHEMA
    )

    op.create_table('subvenciones_administraciones',
        *audit_columns(),
        sa.Column('subvencion_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.intervenciones_subvenciones.id'), index=True, nullable=False),
        sa.Column('administracion_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.administraciones.id'), index=True, nullable=False),
        sa.Column('importe_aportado', sa.Numeric(15, 2)),
        sa.Column('porcentaje_participacion', sa.Numeric(5, 2)),
        schema=SCHEMA
    )

    # =========================================================================
    # 14. OSM PLACES
    # =========================================================================

    op.create_table('osm_places',
        *audit_columns(),
        sa.Column('osm_id', sa.String(50), unique=True, index=True, nullable=False),
        sa.Column('name', sa.String(255), index=True, nullable=False),
        sa.Column('amenity', sa.String(100), index=True),
        sa.Column('religion', sa.String(50)),
        sa.Column('denomination', sa.String(100)),
        sa.Column('municipio_id', sa.String(36), index=True),
        sa.Column('addr_city', sa.String(100)),
        sa.Column('addr_postcode', sa.String(20)),
        sa.Column('geom', Geometry(geometry_type='POINT', srid=4326), nullable=False),
        sa.Column('tags', postgresql.JSONB()),
        schema=SCHEMA
    )

    # =========================================================================
    # 15. DISCOVERY (PORTALS)
    # =========================================================================

    op.create_table('portals_inmuebles_raw',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('portal', sa.String(50), nullable=False),
        sa.Column('id_portal', sa.String(100), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('titulo', sa.Text()),
        sa.Column('descripcion', sa.Text()),
        sa.Column('tipo', sa.String(100)),
        sa.Column('precio', sa.Numeric(12, 2)),
        sa.Column('superficie', sa.Numeric(10, 2)),
        sa.Column('geo_type', sa.String(20), nullable=False),
        sa.Column('lat', sa.Numeric(10, 7)),
        sa.Column('lon', sa.Numeric(10, 7)),
        sa.Column('geom', Geometry(geometry_type='POINT', srid=4326)),
        sa.Column('direccion', sa.Text()),
        sa.Column('ciudad', sa.String(200)),
        sa.Column('provincia', sa.String(200)),
        sa.Column('scraped_at', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        schema=SCHEMA
    )

    op.create_table('portals_detecciones',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('inmueble_id', sa.Integer(), sa.ForeignKey(f'{SCHEMA}.portals_inmuebles_raw.id'), index=True, nullable=False),
        sa.Column('inmueble_core_id', sa.String(36), sa.ForeignKey(f'{SCHEMA}.inmuebles.id'), index=True),
        sa.Column('score', sa.Numeric(5, 2), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('evidences', postgresql.JSONB()),
        sa.Column('first_detected_at', sa.DateTime(), nullable=False),
        sa.Column('last_updated_at', sa.DateTime(), nullable=False),
        sa.Column('confirmed_at', sa.DateTime()),
        schema=SCHEMA
    )


def downgrade() -> None:
    # Discovery
    op.drop_table('portals_detecciones', schema=SCHEMA)
    op.drop_table('portals_inmuebles_raw', schema=SCHEMA)

    # OSM
    op.drop_table('osm_places', schema=SCHEMA)

    # Subvenciones
    op.drop_table('subvenciones_administraciones', schema=SCHEMA)
    op.drop_table('intervenciones_subvenciones', schema=SCHEMA)

    # Intervenciones
    op.drop_table('intervenciones_tecnicos', schema=SCHEMA)
    op.drop_table('intervenciones', schema=SCHEMA)

    # Transmisiones
    op.drop_table('transmision_anunciantes', schema=SCHEMA)
    op.drop_table('transmisiones', schema=SCHEMA)

    # Documentos
    op.drop_table('inmuebles_documentos', schema=SCHEMA)
    op.drop_table('documentos', schema=SCHEMA)

    # Inmuebles
    op.drop_table('inmuebles_niveles_proteccion', schema=SCHEMA)
    op.drop_table('inmuebles_usos', schema=SCHEMA)
    op.drop_table('citas_bibliograficas', schema=SCHEMA)
    op.drop_table('inmuebles_wd_ext', schema=SCHEMA)
    op.drop_table('inmuebles_osm_ext', schema=SCHEMA)
    op.drop_table('inmuebles_denominaciones', schema=SCHEMA)
    op.drop_table('inmatriculaciones', schema=SCHEMA)
    op.drop_table('inmuebles', schema=SCHEMA)

    # Historiografía
    op.drop_table('fuentes_historiograficas', schema=SCHEMA)

    # Actores
    op.drop_table('agencias_inmobiliarias', schema=SCHEMA)
    op.drop_table('entidades_religiosas_titulares', schema=SCHEMA)
    op.drop_table('entidades_religiosas', schema=SCHEMA)
    op.drop_table('registros_propiedad_titulares', schema=SCHEMA)
    op.drop_table('registros_propiedad', schema=SCHEMA)
    op.drop_table('notarias_titulares', schema=SCHEMA)
    op.drop_table('notarias', schema=SCHEMA)
    op.drop_table('diocesis_titulares', schema=SCHEMA)
    op.drop_table('diocesis', schema=SCHEMA)
    op.drop_table('administraciones_titulares', schema=SCHEMA)
    op.drop_table('administraciones', schema=SCHEMA)
    op.drop_table('tecnicos', schema=SCHEMA)
    op.drop_table('colegios_profesionales', schema=SCHEMA)
    op.drop_table('privados', schema=SCHEMA)

    # Geografía
    op.drop_table('tipos_figura_proteccion', schema=SCHEMA)
    op.drop_table('municipios', schema=SCHEMA)
    op.drop_table('provincias', schema=SCHEMA)
    op.drop_table('comunidades_autonomas', schema=SCHEMA)

    # Tipologías
    op.drop_table('fuentes_documentales', schema=SCHEMA)
    op.drop_table('tipos_licencia', schema=SCHEMA)
    op.drop_table('tipos_mime_documento', schema=SCHEMA)
    op.drop_table('tipos_titulo_propiedad', schema=SCHEMA)
    op.drop_table('tipos_uso_inmueble', schema=SCHEMA)
    op.drop_table('tipos_entidad_religiosa', schema=SCHEMA)
    op.drop_table('tipos_via', schema=SCHEMA)
    op.drop_table('tipos_transmision', schema=SCHEMA)
    op.drop_table('tipos_persona', schema=SCHEMA)
    op.drop_table('tipos_inmueble', schema=SCHEMA)
    op.drop_table('tipos_documento', schema=SCHEMA)
    op.drop_table('tipos_certificacion_propiedad', schema=SCHEMA)
    op.drop_table('roles_tecnico', schema=SCHEMA)
    op.drop_table('estados_tratamiento', schema=SCHEMA)
    op.drop_table('estados_conservacion', schema=SCHEMA)

    # Usuarios
    op.drop_table('usuario_rol', schema=SCHEMA)
    op.drop_table('roles', schema=SCHEMA)
    op.drop_table('usuarios', schema=SCHEMA)

    # Enums
    op.execute(f'DROP TYPE IF EXISTS {SCHEMA}.nivel_proteccion')
    op.execute(f'DROP TYPE IF EXISTS {SCHEMA}.tipoidentificacion')

    # Schema
    op.execute(f'DROP SCHEMA IF EXISTS {SCHEMA} CASCADE')
