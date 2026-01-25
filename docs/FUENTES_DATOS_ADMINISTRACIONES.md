# Fuentes de Datos - Administraciones por Comunidad Autónoma

## FUENTE PRINCIPAL: DIR3 (Directorio Común de Unidades Orgánicas y Oficinas)

**RECOMENDACIÓN: Usar DIR3 como fuente primaria para todas las administraciones públicas españolas**

- **Portal oficial**: https://administracionelectronica.gob.es/ctt/dir3/descargas
- **Catálogo datos.gob.es**: https://datos.gob.es/es/catalogo/e05188501-directorio-comun-de-unidades-organicas-y-oficinas-dir3
- **Descripción**: Inventario unificado de todas las Administraciones de unidades orgánicas/organismos públicos, oficinas asociadas y unidades de gestión económico-presupuestaria
- **Alcance**: TODAS las comunidades autónomas, administración estatal, local y universidades
- **Formato**: XLSX (Excel) - 17 distribuciones disponibles
- **Actualización**: Mensual aproximadamente
- **Archivos disponibles**:
  - Catálogo de Comunidades Autónomas
  - Catálogo de Localidades
  - Catálogo de Provincias
  - Catálogo de Tipos de Unidades Orgánicas
  - Información Básica de Unidades de Gestión Económico-Presupuestaria (UGEP) por niveles de administración
  - Información Básica de Unidades Orgánicas por niveles de administración
  - Información Básica de Unidades Universitarias
  - Catálogo de Servicios de Oficinas
- **Licencia**: https://administracionelectronica.gob.es/pae_Home/pae_Informacion/pae_AvisoLegal.html
- **Calidad**: ⭐⭐⭐⭐⭐ - Fuente oficial del Estado
- **Ventajas**:
  - Única fuente centralizada para todas las CCAA
  - Actualización regular y oficial
  - Estructura jerárquica completa
  - Códigos DIR3 oficiales (necesarios para facturación electrónica FACe)
  - Mantenimiento distribuido y co-responsable
- **Desventajas**:
  - Formato XLSX (requiere conversión)
  - No tiene API REST (solo descargas de archivos)
  - Puede no incluir titulares de los órganos (solo estructura)

---

## FUENTES COMPLEMENTARIAS POR COMUNIDAD AUTÓNOMA

Las siguientes fuentes pueden usarse como **complemento a DIR3** para obtener información adicional como titulares, biografías, funciones detalladas, etc.

## Aragón
- **API Base**: https://opendata.aragon.es/api/action/
- **Dataset**: Organigrama del Gobierno de Aragón (ID: 43cd95f6-6b93-4510-b652-7ad8d74f78ca)
- **Recursos principales**:
  - **Entidades** (CSV): https://opendata.aragon.es/GA_OD_Core/download?resource_id=159&formato=csv
  - **Entidades** (JSON): https://opendata.aragon.es/GA_OD_Core/download?resource_id=159&formato=json
  - **Cargos** (CSV): https://opendata.aragon.es/GA_OD_Core/download?resource_id=160&formato=csv
  - **Cargos** (JSON): https://opendata.aragon.es/GA_OD_Core/download?resource_id=160&formato=json
  - **Períodos** (CSV): https://opendata.aragon.es/GA_OD_Core/download?resource_id=158&formato=csv
- **Licencia**: CC-BY-4.0
- **Actualización**: Anual
- **Nota**: Contiene consejerías, direcciones generales, servicios y cargos desde 1979

## Andalucía
- **URL directa (CSV)**: https://www.juntadeandalucia.es/ssdigitales/festa/download-pro/dataset-datos_basicos.csv
- **Contenido**: Órganos administrativos completos (consejerías, direcciones generales, delegaciones territoriales, servicios)
- **Columnas**: cod_dir3, title, responsable, division, directing_center, functions, biography, ref_dir3, status
- **Utilidad**: Muy alta - contiene jerarquía completa, titulares, funciones y competencias
- **Actualización**: Regular (datos básicos oficiales)

## Asturias
- **Estructura**: https://datos.gob.es/es/catalogo/a03002951-estructuras-organicas
- **Titulares**: No disponible

## Baleares
- **Estructura y Titulares (PDF)**: https://www.caib.es/sites/estructura2019/f/429866
- **Formato**: PDF con organigrama completo
- **Nota**: Requiere extracción desde PDF

## Cantabria
- **API**: https://www.icane.es/statviewer-backend/api/
- **Estado**: API vacía o sin documentación accesible
- **Nota**: Instituto Cántabro de Estadística - enfocado en datos estadísticos, no estructura administrativa

## Castilla-La Mancha
- **URL (HTML/Tabla)**: https://www.castillalamancha.es/gobierno/directorio/xls
- **Formato**: Tabla HTML estructurada (no es XLS, a pesar del nombre de la URL)
- **Contenido**: ~200 registros con 11 consejerías y delegaciones provinciales
- **Columnas**: Organismo (1ª y 2ª nivel), Titular, Cargo, Dirección, Teléfono, Fax, Email, Facebook, LinkedIn, Twitter
- **Cobertura**: Presidencia, vicepresidencias, consejerías, organismos dependientes y delegaciones (Albacete, Ciudad Real, Cuenca, Guadalajara, Toledo)
- **Utilidad**: Alta - directorio oficial completo con jerarquía y contactos

## Catalunya
- **API Base**: https://www.idescat.cat/dev/api/?lang=es
- **Tipo**: APIs RESTful del Institut d'Estadística de Catalunya (Idescat)
- **APIs disponibles**:
  - Tables (v2): `/dev/api/taules/`
  - Daily Indicators (v1): `/dev/api/indicadors/`
  - Population Search (v1): `/dev/api/pob/`
  - Municipality Data (v1): `/dev/api/emex/`
  - Y otras 5 APIs más
- **Enfoque**: Datos estadísticos, demográficos, económicos y territoriales
- **Nota**: No contiene estructura administrativa organizativa - enfocado en estadísticas públicas

## Resumen de Calidad de Fuentes

| Comunidad | Calidad | Formato | Actualización | Estado |
|-----------|---------|---------|---------------|--------|
| Aragón | ⭐⭐⭐⭐⭐ | API/CSV/JSON | Anual | ✅ Listo |
| Andalucía | ⭐⭐⭐⭐⭐ | CSV | Regular | ✅ Listo |
| Castilla-La Mancha | ⭐⭐⭐⭐ | HTML | Manual | ⚠️ Requiere scraping |
| Baleares | ⭐⭐⭐ | PDF | Manual | ⚠️ Requiere OCR/extracción |
| Asturias | ⭐⭐ | datos.gob.es | Desconocida | ⚠️ Por verificar |
| Catalunya | ⭐ | N/A | N/A | ❌ Sin fuente administrativa |
| Cantabria | ⭐ | N/A | N/A | ❌ Sin fuente administrativa |

## Galicia

- **Portal Open Data**: https://abertos.xunta.gal/portada
- **Dataset**: Directorio Oficial de la Xunta de Galicia
- **URL directa (CSV)**: https://ficheiros-web.xunta.gal/abertos/dirof/DIROF.csv
- **Portal transparencia**: https://transparencia.xunta.gal/tema/transparencia-institucional/goberno-e-altos-cargos/composicion-do-goberno
- **Formato**: CSV desde portal open data, PDF organigramas desde portal transparencia
- **Contenido**: Directorio oficial con unidades administrativas
- **Nota**: Portal Abert@s usa CKAN pero no tiene API expuesta. Los organigramas están en PDF en el portal de transparencia

## Próximos Pasos Recomendados

### ESTRATEGIA RECOMENDADA:

**1. Implementar ETL para DIR3 (PRIORIDAD MÁXIMA)**
   - Descargar los 17 archivos XLSX de DIR3
   - Parsear Excel y extraer:
     - Unidades Orgánicas de Comunidades Autónomas
     - Jerarquía completa (padre-hijo)
     - Códigos DIR3 oficiales
     - Tipos de unidades orgánicas
   - Poblar modelo `Administracion` con:
     - `codigo_oficial` = código DIR3
     - `nivel_jerarquico` = AUTONOMICO, PROVINCIAL, LOCAL según corresponda
     - `tipo_organo` = tipo de unidad del catálogo DIR3
     - `administracion_padre_id` = jerarquía desde DIR3
   - Ventaja: Cubre TODAS las CCAA de una vez

**2. Fuentes complementarias para titulares (SECUNDARIO)**
   - Andalucía: CSV con responsables y biografías
   - Aragón: API con cargos y períodos
   - Castilla-La Mancha: HTML scraping con titulares
   - Galicia: CSV de directorio oficial
   - Usar estas fuentes para enriquecer datos DIR3 con información de titulares

**3. Actualización periódica**
   - DIR3 se actualiza mensualmente
   - Implementar scheduler para descargar y actualizar automáticamente
   - Marcar unidades que desaparecen con `activa=False` y `valido_hasta=now()`

### Pasos anteriores (ahora secundarios):

1. ~~**Implementar ETL para Aragón** con nuevas URLs (Entidades + Cargos)~~ → Usar DIR3 primero
2. ~~**Actualizar ETL de Andalucía** con nueva URL directa~~ → Usar como complemento para titulares
3. ~~**Crear extractor para Castilla-La Mancha** (scraping HTML)~~ → Usar como complemento para titulares
4. ~~**Investigar Asturias**~~ → Ya cubierto por DIR3
5. ~~**Buscar fuentes para Catalunya y Cantabria**~~ → Ya cubierto por DIR3
6. ~~**Resto de comunidades autónomas**~~ → Ya cubierto por DIR3
