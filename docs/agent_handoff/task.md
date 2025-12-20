# Tasks: SIPI Intelligence System Implementation

- [/] Planning & Architecture <!-- id: 0 -->
    - [x] Analyze `sipi-survey` capabilities <!-- id: 1 -->
    - [x] Design Surveillance & Detection Workflows <!-- id: 2 -->
    - [x] Create Implementation Plan <!-- id: 3 -->

- [ ] Phase 1: Core Architecture (Foundation) <!-- id: 4 -->
    - [ ] **[Backend]** Create `OSMPlace` model in `sipi-core` <!-- id: 5 -->
    - [ ] **[Backend]** Create `InmuebleLifecycle` model (History/Events) <!-- id: 6 -->
    - [ ] **[Backend]** Update `Inmueble` model <!-- id: 7 -->
        - [ ] Status Enum & GeoQuality
        - [ ] Visitability (`es_visitable`, `horario_visitas`)
    - [ ] **[Backend]** Implement GQL Mutations with BIC Validation <!-- id: 8 -->

- [ ] Phase 2: Surveillance Engines (The "Eyes") <!-- id: 9 -->
    - [ ] **[ETL]** Create `osm_census_loader` script (Bulk Import) <!-- id: 10 -->
    - [ ] **[Survey]** Implement `SubsidyScraper` (NIF 'R%') <!-- id: 11 -->
    - [ ] **[Survey]** Implement `ProcurementScraper` (Contratación Estado) <!-- id: 12 -->
    - [ ] **[ETL]** Create `AutoMatcher` pipeline (Matching Logic) <!-- id: 13 -->

- [ ] Phase 3: Intelligence Console (Frontend) <!-- id: 14 -->
    - [ ] **[UI]** Create `GeoMatcher` View (Resolver Geolocation) <!-- id: 15 -->
    - [ ] **[UI]** Create `Opportunities` View (Ads/Subsidies) <!-- id: 16 -->
    - [ ] **[UI]** Update `InmuebleForm` (Visitability Section + BIC Validation) <!-- id: 17 -->
    - [ ] **[UI]** Implement `LifecycleTimeline` Component <!-- id: 18 -->

- [ ] Phase 4: Integration <!-- id: 19 -->
    - [ ] **[Integration]** Verify end-to-end flow: Subsidy -> Notification -> History Update <!-- id: 20 -->
