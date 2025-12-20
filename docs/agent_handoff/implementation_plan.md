# Implementation Plan - SIPI Global (Core + Survey + Frontend)

# Goal Description
Enhance SIPI to become a proactive Intelligence System. It will catalog properties, track their complex history (ownership, rehabs, subsidies), and actively surveil external sources to detect status changes.
**Key Addition**: Support for "Visitability" regimes, specifically enforcing Visiting Schedules (`Horario de Visitas`) for properties declared as BIC (Bien de Interés Cultural).

## User Review Required
> [!IMPORTANT]
> **Data Strategy: Hybrid Persistence for Surveillance**
> 1. **OSM Reference Census**: Saved locally in `sipi-core`. Used for Geolocation.
> 2. **Surveillance "Signals"**: Scraped ads/subsidies saved in `sipi-survey` (Staging).
> 3. **Consolidated Intelligence**: Validated matches promoted to `sipi-core`.

> [!NOTE]
> **Visitability Rule**: Properties marked as `BIC` (Bien de Interés Cultural) and `Visitable` MUST have a defined `Visiting Schedule`.

## Proposed Changes

### Phase 1: Core Architecture & Data Quality (Week 1)
Establish the foundation for handling lifecycle, geolocation, and visitability.

#### `sipi-core`
- **[NEW] `sipi/db/models/osm.py`**: Model `OSMPlace` for local reference census.
- **[NEW] `sipi/db/models/lifecycle.py`**: Model `InmuebleLifecycle` to track `INMATRICULADO` -> `EN_VENTA`.
- **[MODIFY] `sipi/db/models/inmuebles.py`**:
    - Add `estado_ciclo_vida` (Enum: `INMATRICULADO`, `EN_VENTA`, `VENDIDO`, `CAMBIO_USO`).
    - Add `geo_quality` (Enum).
    - Add `es_visitable` (Boolean).
    - Add `horario_visitas` (Text/JSON).
    - Add `enlace_web_visitas` (URL - Optional).
- **[MODIFY] `sipi-api/app/graphql`**: Mutations to handle these new fields and validate BIC requirements.

### Phase 2: Surveillance Engines (Week 2)
Activate the "eyes" of the system (`sipi-survey`).

#### `sipi-survey` & `sipi-etl`
- **[NEW] `pipelines/osm_census_loader.py`**: Script to bulk load OSM data.
- **[NEW] `src/modules/subsidies`**: Scraper for subsidies (NIF 'R%'). linking to `InmuebleLifecycle` (Event: `REHABILITACION_SUBVENCIONADA`).
- **[NEW] `src/modules/procurement`**: Scraper for Public Contracts.
- **[NEW] `pipelines/auto_matcher.py`**: Logic for "Posiblemente Vendido" and linking ads.

### Phase 3: Intelligence Console (Week 3)
Give the user control over the automated findings.

#### `sipi-frontend`
- **[NEW] `src/modules/discovery/views/GeoMatcher.vue`**: UI to manually validate low-confidence detections.
- **[NEW] `src/modules/discovery/views/Opportunities.vue`**: Feed of Subsidies/Contracts.
- **[NEW] `src/modules/inmuebles/components/LifecycleTimeline.vue`**: Visualize history: Construction -> Inmatriculación -> **Subsidies (Rehab)** -> Sales.
- **[MODIFY] `src/modules/inmuebles/components/InmuebleForm.vue`**:
    - Add "Régimen de Visitas" section.
    - **Validation**: If `FiguraProteccion == BIC` AND `Visitable == true`, field `Horario` is mandatory.

## Workflow: From Detection to Action
1.  **Survey**: Detects an ad or a Subsidy Grant ("Restoration of Roof").
2.  **Auto-Matcher**: Links subsidy to "Convento de Santa Fe".
3.  **Frontend**: User confirms.
4.  **Result**:
    - Property History gets a new event: `REHABILITACION` (Source: Subsidy).
    - System prompts to verify if "Visitability" status changed due to public funding.

## Verification Plan
### Automated Tests
- Test `Inmueble` validation: Fail if BIC + Visitable has no Schedule.
- Test `Lifecycle` flow: Detect Subsidy -> Add Event.

### Manual Verification
- **Surveillance**: Run subsidy scraper. Confirm finding appears in "Opportunities".
- **Visitability**: Edit a BIC property, set "Visitable" = true, leave Schedule empty. Verify UI blocks saving.
