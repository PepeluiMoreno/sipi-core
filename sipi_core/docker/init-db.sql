-- Inicializacion de la base de datos SIPI
-- Este script se ejecuta automaticamente al crear el contenedor

-- Crear extension PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- Crear schemas
CREATE SCHEMA IF NOT EXISTS sipi;
CREATE SCHEMA IF NOT EXISTS portals;

-- Dar permisos al usuario
GRANT ALL PRIVILEGES ON SCHEMA sipi TO sipi;
GRANT ALL PRIVILEGES ON SCHEMA portals TO sipi;
