# Tasks: SIPI Intelligence System Implementation

- [x] Planning & Architecture <!-- id: 0 -->
    - [x] Analyze `sipi-survey` capabilities <!-- id: 1 -->
    - [x] Design Surveillance & Detection Workflows <!-- id: 2 -->
    - [x] Create Implementation Plan <!-- id: 3 -->

- [x] Phase 1: Core Architecture (Foundation) <!-- id: 4 -->
    - [x] **[Backend]** Create `OSMPlace` model in `sipi-core` <!-- id: 5 -->
    - [x] **[Backend]** Create `InmuebleLifecycle` model (History/Events) <!-- id: 6 -->
    - [x] **[Backend]** Update `Inmueble` model <!-- id: 7 -->
        - [x] Status Enum & GeoQuality
        - [x] Visitability (`es_visitable`, `horario_visitas`)
    - [x] **[Backend]** Configure GraphQL auto-generation for new models <!-- id: 8 -->
    - [x] **[Backend]** Create Alembic migration <!-- id: 9 -->
    - [ ] **[Backend]** Apply migration to Aiven DB (pending DB activation) <!-- id: 10 -->

- [ ] Phase 2: Surveillance Engines (The "Eyes") <!-- id: 11 -->
    - [ ] **[ETL]** Create `lista_geografica_loader` script (Bulk Import) <!-- id: 12 -->
    - [ ] **[Survey]** Implement `SubsidyScraper` (NIF 'R%') <!-- id: 13 -->
    - [ ] **[Survey]** Implement `ProcurementScraper` (Contratación Estado) <!-- id: 14 -->
    - [ ] **[ETL]** Create `AutoMatcher` pipeline (Matching Logic) <!-- id: 15 -->

- [ ] Phase 3: Intelligence Console (Frontend) <!-- id: 16 -->
    - [ ] **[UI]** Create `GeoMatcher` View (Resolver Geolocation) <!-- id: 17 -->
    - [ ] **[UI]** Create `Opportunities` View (Ads/Subsidies) <!-- id: 18 -->
    - [ ] **[UI]** Update `InmuebleForm` (Visitability Section + BIC Validation) <!-- id: 19 -->
    - [ ] **[UI]** Implement `LifecycleTimeline` Component <!-- id: 20 -->

- [ ] Phase 4: Integration <!-- id: 21 -->
    - [ ] **[Integration]** Verify end-to-end flow: Subsidy -> Notification -> History Update <!-- id: 22 -->
