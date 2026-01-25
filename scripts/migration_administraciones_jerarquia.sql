-- Migración: Agregar jerarquía y enriquecimiento de administraciones
-- Fecha: 2026-01-02
-- Descripción: Agrega estructura jerárquica a administraciones y datos de contacto a titulares

-- ============================================================================
-- PASO 1: Modificar tabla administraciones
-- ============================================================================

-- Eliminar constraint de unique en nombre (puede haber órganos con mismo nombre en diferentes niveles)
ALTER TABLE administraciones DROP CONSTRAINT IF EXISTS administraciones_nombre_key;

-- Agregar nuevas columnas para jerarquía
ALTER TABLE administraciones
    ADD COLUMN IF NOT EXISTS codigo_oficial VARCHAR(100) UNIQUE,
    ADD COLUMN IF NOT EXISTS administracion_padre_id VARCHAR(36),
    ADD COLUMN IF NOT EXISTS nivel_jerarquico VARCHAR(50),
    ADD COLUMN IF NOT EXISTS tipo_organo VARCHAR(100),
    ADD COLUMN IF NOT EXISTS orden_jerarquico INTEGER,
    ADD COLUMN IF NOT EXISTS activa BOOLEAN DEFAULT TRUE NOT NULL;

-- Crear índices para jerarquía
CREATE INDEX IF NOT EXISTS idx_administraciones_padre_id ON administraciones(administracion_padre_id);
CREATE INDEX IF NOT EXISTS idx_administraciones_nivel_jerarquico ON administraciones(nivel_jerarquico);
CREATE INDEX IF NOT EXISTS idx_administraciones_tipo_organo ON administraciones(tipo_organo);
CREATE INDEX IF NOT EXISTS idx_administraciones_orden_jerarquico ON administraciones(orden_jerarquico);
CREATE INDEX IF NOT EXISTS idx_administraciones_activa ON administraciones(activa);
CREATE INDEX IF NOT EXISTS idx_administraciones_codigo_oficial ON administraciones(codigo_oficial);

-- Agregar foreign key para jerarquía (auto-referencia)
ALTER TABLE administraciones
    ADD CONSTRAINT fk_administracion_padre
    FOREIGN KEY (administracion_padre_id)
    REFERENCES administraciones(id)
    ON DELETE SET NULL;

-- ============================================================================
-- PASO 2: Modificar tabla administraciones_titulares - Agregar datos de contacto
-- ============================================================================

-- Agregar campos de contacto (ContactoMixin)
ALTER TABLE administraciones_titulares
    ADD COLUMN IF NOT EXISTS email_personal VARCHAR(255),
    ADD COLUMN IF NOT EXISTS email_corporativo VARCHAR(255),
    ADD COLUMN IF NOT EXISTS telefono VARCHAR(20),
    ADD COLUMN IF NOT EXISTS telefono_movil VARCHAR(20),
    ADD COLUMN IF NOT EXISTS fax VARCHAR(20),
    ADD COLUMN IF NOT EXISTS sitio_web VARCHAR(500),
    ADD COLUMN IF NOT EXISTS notas VARCHAR(500);

-- Agregar campos de dirección (DireccionMixin)
ALTER TABLE administraciones_titulares
    ADD COLUMN IF NOT EXISTS direccion VARCHAR(255),
    ADD COLUMN IF NOT EXISTS codigo_postal VARCHAR(10),
    ADD COLUMN IF NOT EXISTS localidad VARCHAR(100),
    ADD COLUMN IF NOT EXISTS comunidad_autonoma_id VARCHAR(36),
    ADD COLUMN IF NOT EXISTS provincia_id VARCHAR(36),
    ADD COLUMN IF NOT EXISTS municipio_id VARCHAR(36);

-- Crear índices para contacto
CREATE INDEX IF NOT EXISTS idx_administraciones_titulares_email_personal ON administraciones_titulares(email_personal);
CREATE INDEX IF NOT EXISTS idx_administraciones_titulares_email_corporativo ON administraciones_titulares(email_corporativo);

-- Crear índices para dirección
CREATE INDEX IF NOT EXISTS idx_administraciones_titulares_codigo_postal ON administraciones_titulares(codigo_postal);
CREATE INDEX IF NOT EXISTS idx_administraciones_titulares_comunidad_autonoma_id ON administraciones_titulares(comunidad_autonoma_id);
CREATE INDEX IF NOT EXISTS idx_administraciones_titulares_provincia_id ON administraciones_titulares(provincia_id);
CREATE INDEX IF NOT EXISTS idx_administraciones_titulares_municipio_id ON administraciones_titulares(municipio_id);

-- Agregar foreign keys geográficas
ALTER TABLE administraciones_titulares
    ADD CONSTRAINT fk_administraciones_titulares_comunidad_autonoma
    FOREIGN KEY (comunidad_autonoma_id)
    REFERENCES comunidades_autonomas(id)
    ON DELETE SET NULL;

ALTER TABLE administraciones_titulares
    ADD CONSTRAINT fk_administraciones_titulares_provincia
    FOREIGN KEY (provincia_id)
    REFERENCES provincias(id)
    ON DELETE SET NULL;

ALTER TABLE administraciones_titulares
    ADD CONSTRAINT fk_administraciones_titulares_municipio
    FOREIGN KEY (municipio_id)
    REFERENCES municipios(id)
    ON DELETE SET NULL;

-- ============================================================================
-- PASO 3: Actualizar datos existentes (opcional)
-- ============================================================================

-- Marcar todas las administraciones existentes como activas
UPDATE administraciones SET activa = TRUE WHERE activa IS NULL;

-- ============================================================================
-- COMENTARIOS Y DOCUMENTACIÓN
-- ============================================================================

COMMENT ON COLUMN administraciones.codigo_oficial IS 'Código oficial de la administración (único)';
COMMENT ON COLUMN administraciones.administracion_padre_id IS 'FK a la administración padre (jerarquía)';
COMMENT ON COLUMN administraciones.nivel_jerarquico IS 'Nivel jerárquico: ESTATAL, AUTONOMICO, PROVINCIAL, LOCAL';
COMMENT ON COLUMN administraciones.tipo_organo IS 'Tipo de órgano: CONSEJERIA, DIRECCION_GENERAL, SERVICIO, etc.';
COMMENT ON COLUMN administraciones.orden_jerarquico IS 'Orden dentro del mismo nivel jerárquico';
COMMENT ON COLUMN administraciones.activa IS 'Indica si la administración está activa';

COMMENT ON COLUMN administraciones_titulares.email_personal IS 'Email personal del titular';
COMMENT ON COLUMN administraciones_titulares.email_corporativo IS 'Email corporativo del titular';
COMMENT ON COLUMN administraciones_titulares.telefono IS 'Teléfono fijo del titular';
COMMENT ON COLUMN administraciones_titulares.telefono_movil IS 'Teléfono móvil del titular';
