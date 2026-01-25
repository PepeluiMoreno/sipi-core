# SIPI Project Documentation

This directory contains key documentation for the SIPI project, intended to help agents and developers understand the current status and roadmap.

## 📍 Current Status

**Phase 1: Core Architecture** - ✅ **COMPLETED** (2025-12-21)

See [PHASE1_COMPLETED.md](PHASE1_COMPLETED.md) for detailed implementation report.

**Sistema de Procesos e Historial - Decisión Arquitectónica** - ✅ **COMPLETED** (2026-01-05)

Se ha decidido NO implementar un sistema genérico de procesos. En su lugar:
- Se utilizan 3 modelos específicos: `Inmatriculacion`, `Transmision`, `Actuacion`
- Propiedad computada `timeline_procesos` en `Inmueble` para timeline unificado
- Modelo `EventoHistorial` para eventos detectados automáticamente (historial del inmueble)

See [ARQUITECTURA_HISTORIAL_INMUEBLES.md](ARQUITECTURA_HISTORIAL_INMUEBLES.md) for complete architectural decision documentation.

---

## Key Documents

- **[Implementation Plan](implementation_plan.md)**: Detailed plan for all phases (Intelligence System, Visitability, Geolocation).
- **[Task List](task.md)**: Granular checklist of tasks and their status (auto-updated).
- **[Phase 1 Completed](PHASE1_COMPLETED.md)**: Complete report of Phase 1 implementation with file locations and technical details.
- **[Arquitectura Historial Inmuebles](ARQUITECTURA_HISTORIAL_INMUEBLES.md)**: ⭐ NEW - Architectural decision for process management and property history system (2026-01-05).

---

## Project Structure

- `sipi-core`: Shared domain models and logic.
- `sipi-api`: Backend API (FastAPI + Strawberry GraphQL).
- `sipi-frontend`: Vue 3 + Tailwind CSS Frontend.
- `sipi-survey`: Scrapers and ETL pipelines.

---

## Quick Start for Agents

1. **Read** [PHASE1_COMPLETED.md](PHASE1_COMPLETED.md) to understand what's been implemented
2. **Check** [task.md](task.md) for current task status
3. **Review** [implementation_plan.md](implementation_plan.md) for overall architecture
4. **Continue** with Phase 2 tasks from [task.md](task.md)
