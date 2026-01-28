-- alembic/init_postgis.sql
-- Este script se ejecuta ANTES de las migraciones
-- para crear las extensiones necesarias

-- 1. Crear extensión PostGIS (requiere superusuario)
--    Si no tienes permisos, ejecútalo manualmente como postgres primero
DO $$
BEGIN
    -- Intentar crear la extensión
    BEGIN
        CREATE EXTENSION IF NOT EXISTS postgis;
        RAISE NOTICE '✅ Extensión PostGIS creada/verificada';
    EXCEPTION WHEN insufficient_privilege THEN
        RAISE WARNING '⚠️  No se pudo crear PostGIS. Ejecuta manualmente como superusuario:';
        RAISE WARNING '    sudo -u postgres psql -d % -c "CREATE EXTENSION postgis;"', current_database();
        RAISE WARNING '    sudo -u postgres psql -d % -c "CREATE EXTENSION postgis_topology;"', current_database();
    END;
END
$$;

-- 2. Crear schema principal si no existe
CREATE SCHEMA IF NOT EXISTS sipi;

-- 3. Otorgar permisos básicos al usuario actual
GRANT USAGE ON SCHEMA sipi TO CURRENT_USER;
GRANT CREATE ON SCHEMA sipi TO CURRENT_USER;

-- 4. Crear tabla de versión de extensiones (opcional)
CREATE TABLE IF NOT EXISTS sipi.extension_versions (
    id SERIAL PRIMARY KEY,
    extension_name VARCHAR(100) NOT NULL,
    version VARCHAR(50) NOT NULL,
    installed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(extension_name)
);

-- 5. Registrar versión de PostGIS si existe
DO $$
DECLARE
    postgis_version TEXT;
BEGIN
    SELECT PostGIS_Version() INTO postgis_version;
    IF postgis_version IS NOT NULL THEN
        INSERT INTO sipi.extension_versions (extension_name, version)
        VALUES ('postgis', postgis_version)
        ON CONFLICT (extension_name) 
        DO UPDATE SET version = EXCLUDED.version, installed_at = CURRENT_TIMESTAMP;
        RAISE NOTICE '✅ PostGIS versión % registrada', postgis_version;
    END IF;
EXCEPTION WHEN OTHERS THEN
    -- Ignorar errores si PostGIS no está disponible
    NULL;
END
$$;