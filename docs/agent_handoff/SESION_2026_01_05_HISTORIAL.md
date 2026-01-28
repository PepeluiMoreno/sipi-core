# Sesión 2026-01-05: Implementación del Sistema de Historial de Inmuebles

**Fecha**: 2026-01-05
**Duración**: ~2 horas
**Estado**: ✅ COMPLETADO (pendiente aplicar migración)

---

## 📋 Resumen de la Sesión

En esta sesión se tomó la decisión arquitectónica de **NO implementar un sistema genérico de procesos** y en su lugar se optó por:
1. Mantener los 3 modelos específicos existentes: `Inmatriculacion`, `Transmision`, `Actuacion`
2. Agregar propiedad computada `timeline_procesos` para timeline unificado
3. Renombrar `InmuebleLifecycle` → `EventoHistorial` (terminología más española)
4. Eliminar todo el código del sistema de procesos genérico

---

## 🎯 Decisión Arquitectónica Principal

### ❌ Opción Descartada: Sistema Genérico de Procesos

Se había diseñado un sistema complejo con:
- `TipoProceso`, `TipoActor`, `ProcesoInmueble`, `ProcesoActor`, `ProcesoDocumento`
- Tablas de configuración dinámica
- Script de población de catálogos
- 6+ tablas adicionales

**Razones para descartarlo:**
- ✅ Sobrecomplica innecesariamente (ya hay 3 modelos que funcionan)
- ✅ No hay requisito real de extensibilidad (solo 3 tipos de procesos previstos)
- ✅ Añade indirección innecesaria (polimorfismo, lookups dinámicos)
- ✅ Los modelos específicos ya tienen toda la lógica necesaria

### ✅ Solución Implementada: Modelos Específicos + Historial

**3 Modelos para Procesos Formales:**
1. `Inmatriculacion` - Registro inicial de propiedad
2. `Transmision` - Compraventas y transferencias
3. `Actuacion` - Intervenciones físicas (rehabilitaciones)

**Sistema de Historial (Detección Automática):**
- `EventoHistorial` - Eventos detectados por scrapers/ETL
- Almacenado en tabla `historial_inmueble`
- Acceso vía `Inmueble.historial`

**Timeline Unificado:**
- Propiedad computada `Inmueble.timeline_procesos`
- Retorna lista ordenada cronológicamente de todos los procesos

---

## 🔧 Cambios Implementados

### 1. Modelos Creados/Modificados

#### ✅ Nuevo: `EventoHistorial` ([historial.py](../../sipi/db/models/historial.py))

```python
class TipoEventoHistorial(str, Enum):
    """Tipos de eventos detectables automáticamente"""
    ALTA_INMATRICULACION = "alta_inmatriculacion"
    PUESTA_EN_VENTA = "puesta_en_venta"
    VENDIDO = "vendido"
    CAMBIO_DE_USO = "cambio_de_uso"
    REHABILITACION = "rehabilitacion"
    REHABILITACION_SUBVENCIONADA = "rehabilitacion_subvencionada"
    DECLARACION_BIC = "declaracion_bic"
    CAMBIO_VISITABILIDAD = "cambio_visitabilidad"

class EventoHistorial(UUIDPKMixin, AuditMixin, Base):
    """Historial del inmueble: eventos detectados automáticamente"""
    __tablename__ = "historial_inmueble"

    inmueble_id: Mapped[str]
    tipo_evento: Mapped[TipoEventoHistorial]
    fecha_evento: Mapped[datetime]
    detalles: Mapped[Optional[dict]]  # JSONB
    descripcion: Mapped[Optional[str]]
    fuente: Mapped[Optional[str]]  # "Scraper-Idealista", "Scraper-BOE", etc.
```

**Propósito:** Registrar eventos detectados automáticamente por el sistema de inteligencia.

---

#### ✅ Modificado: `Inmueble` ([inmuebles.py](../../sipi/db/models/inmuebles.py))

**Nueva relación:**
```python
# Historial del inmueble (sistema de inteligencia)
historial: Mapped[List["EventoHistorial"]] = relationship(
    "EventoHistorial",
    back_populates="inmueble",
    cascade="all, delete-orphan"
)
```

**Nueva propiedad computada:**
```python
@property
def timeline_procesos(self) -> List[dict]:
    """
    Retorna todos los procesos del inmueble ordenados cronológicamente.

    Incluye: Inmatriculaciones, Transmisiones y Actuaciones.
    """
    eventos = []

    # Inmatriculaciones
    for inmat in self.inmatriculaciones:
        eventos.append({
            'tipo': 'INMATRICULACION',
            'fecha': inmat.fecha_inmatriculacion,
            'id': inmat.id,
            'numero_finca': inmat.numero_finca,
            ...
        })

    # Transmisiones
    for trans in self.transmisiones:
        eventos.append({
            'tipo': 'TRANSMISION',
            'fecha': trans.fecha_transmision,
            'id': trans.id,
            'precio_venta': trans.precio_venta,
            ...
        })

    # Actuaciones
    for act in self.actuaciones:
        eventos.append({
            'tipo': 'ACTUACION',
            'fecha': act.fecha_inicio,
            'id': act.id,
            'nombre': act.nombre,
            ...
        })

    return sorted(eventos, key=lambda x: x['fecha'] or x['created_at'], reverse=True)
```

**Uso desde GraphQL:**
```graphql
query TimelineInmueble($id: ID!) {
  inmueble(id: $id) {
    id
    nombre
    timeline_procesos
  }
}
```

---

### 2. Archivos Eliminados

- ❌ `lifecycle.py` → Renombrado a `historial.py`
- ❌ `scripts/populate_proceso_config.py` - Script de catálogos de procesos genéricos
- ❌ `docs/agent_handoff/MODELO_PROCESOS_REDESIGN.md` - Diseño del sistema genérico
- ❌ `docs/agent_handoff/UI_PROCESOS_DOCUMENTACION.md` - Diseño de UI para procesos
- ❌ `docs/agent_handoff/CLARIFICATION_DOCUMENTOS.md` - Clarificaciones de documentos

---

### 3. Migración de Base de Datos

#### ✅ Creada: `d5e8f9a1b2c3_rename_lifecycle_to_historial_cleanup.py`

**Operaciones de la migración:**

1. **Eliminar tablas del sistema de procesos genérico:**
   - `proceso_documentos`
   - `proceso_actores`
   - `procesos_inmueble`
   - `proceso_tipo_documento_requerido`
   - `proceso_tipo_actor_requerido`
   - `tipos_proceso`
   - `tipos_actor`
   - ENUMs relacionados

2. **Renombrar tabla:**
   ```sql
   ALTER TABLE sipi.inmueble_lifecycle RENAME TO historial_inmueble
   ```

3. **Renombrar ENUM:**
   ```sql
   -- Crear nuevo ENUM
   CREATE TYPE tipoeventohistorial AS ENUM (...)

   -- Cambiar columna
   ALTER TABLE historial_inmueble
   ALTER COLUMN event_type TYPE tipoeventohistorial

   -- Eliminar ENUM antiguo
   DROP TYPE lifecycleeventtype
   ```

4. **Renombrar columnas:**
   - `event_type` → `tipo_evento`
   - `event_date` → `fecha_evento`
   - `details` → `detalles`
   - `description` → `descripcion`
   - `source` → `fuente`

**Ubicación:** [alembic/versions/d5e8f9a1b2c3_rename_lifecycle_to_historial_cleanup.py](../../../sipi-api/alembic/versions/d5e8f9a1b2c3_rename_lifecycle_to_historial_cleanup.py)

**Para aplicar:**
```bash
cd sipi-api
alembic upgrade head
```

---

### 4. Documentación Actualizada

#### ✅ Creado: [ARQUITECTURA_HISTORIAL_INMUEBLES.md](ARQUITECTURA_HISTORIAL_INMUEBLES.md)

Documento completo de decisión arquitectónica que incluye:
- Razones para descartar el sistema genérico
- Descripción de los 3 modelos específicos
- Explicación del sistema de historial
- Diferencias entre procesos formales vs historial
- Comparativa de enfoques
- Lecciones aprendidas

#### ✅ Modificado: [README.md](README.md)

Actualizado el estado del proyecto con la nueva decisión arquitectónica.

#### ✅ Modificado: [PHASE1_COMPLETED.md](PHASE1_COMPLETED.md)

Actualizados todos los nombres de modelos:
- `InmuebleLifecycle` → `EventoHistorial`
- `LifecycleEventType` → `TipoEventoHistorial`
- Referencias a `expediente.py` → `historial.py`

---

## 🔄 Diferencia Clave: Procesos vs Historial

| Aspecto | Procesos (Inmatriculacion, Transmision, Actuacion) | Historial (EventoHistorial) |
|---------|-----------------------------------------------------|------------------------------|
| **Origen** | Ingreso manual por usuarios | Detección automática por scrapers |
| **Formalidad** | Procesos formales con documentación | Eventos informativos/señales |
| **Actores** | Relaciones FK a actores específicos | Solo metadatos en JSON |
| **Propósito** | Registro oficial del inmueble | Inteligencia/vigilancia |
| **Ejemplo** | Escritura de compraventa registrada | Anuncio de venta detectado en Idealista |

---

## 📊 Estructura Final de Archivos

```
sipi-core/
├── sipi/db/models/
│   ├── inmuebles.py         ✅ MODIFICADO - Agregadas: timeline_procesos, historial
│   ├── historial.py         ✅ NUEVO - EventoHistorial, TipoEventoHistorial
│   ├── __init__.py          ✅ MODIFICADO - Exportar nuevos modelos
│   ├── transmisiones.py     ✓ SIN CAMBIOS
│   ├── actuaciones.py       ✓ SIN CAMBIOS
│   └── lifecycle.py         ❌ ELIMINADO - Renombrado a historial.py
│
└── docs/agent_handoff/
    ├── ARQUITECTURA_HISTORIAL_INMUEBLES.md  ✅ NUEVO
    ├── SESION_2026_01_05_HISTORIAL.md       ✅ NUEVO - Este documento
    ├── README.md                             ✅ MODIFICADO
    ├── PHASE1_COMPLETED.md                   ✅ MODIFICADO
    ├── MODELO_PROCESOS_REDESIGN.md          ❌ ELIMINADO
    ├── UI_PROCESOS_DOCUMENTACION.md         ❌ ELIMINADO
    └── CLARIFICATION_DOCUMENTOS.md          ❌ ELIMINADO

sipi-api/
└── alembic/versions/
    └── d5e8f9a1b2c3_rename_lifecycle_to_historial_cleanup.py  ✅ NUEVO

scripts/
└── populate_proceso_config.py  ❌ ELIMINADO
```

---

## ⏭️ Próximos Pasos

### Inmediato
1. ⏳ **Aplicar migración Alembic** (cuando instales Python):
   ```bash
   cd sipi-api
   alembic upgrade head
   ```

2. ⏳ **Verificar migración exitosa:**
   ```bash
   alembic current  # Debe mostrar: d5e8f9a1b2c3
   ```

3. ⏳ **Verificar en BD:**
   ```sql
   -- Verificar tabla renombrada
   \dt sipi.historial_inmueble

   -- Verificar columnas
   \d sipi.historial_inmueble

   -- Verificar ENUM
   \dT+ tipoeventohistorial

   -- Verificar que tablas de procesos genéricos fueron eliminadas
   \dt sipi.*proceso*  -- No debe mostrar nada
   ```

### Corto Plazo (Phase 2)
1. **OSM Census Loader** - Script ETL para cargar lugares desde OpenStreetMap
2. **Subsidy Scraper** - Scraper de subvenciones públicas
3. **Procurement Scraper** - Scraper de contratación pública
4. **AutoMatcher Pipeline** - Lógica de matching automático

Estos scrapers alimentarán la tabla `historial_inmueble` con eventos detectados automáticamente.

---

## 💡 Lecciones Aprendidas

1. **KISS (Keep It Simple)**: No sobre-diseñar cuando modelos específicos son suficientes
2. **YAGNI (You Aren't Gonna Need It)**: No implementar extensibilidad genérica sin requisito claro
3. **Type Safety > Flexibilidad**: En aplicaciones empresariales, preferir tipos explícitos sobre configuración dinámica
4. **Terminología Local**: Usar términos españoles naturales ("Historial" vs "Lifecycle", "Expediente")
5. **Separation of Concerns**: Separar procesos formales (manuales) de eventos automáticos (inteligencia)

---

## 🔗 Referencias

- [Arquitectura Historial Inmuebles](ARQUITECTURA_HISTORIAL_INMUEBLES.md) - Decisión arquitectónica completa
- [Phase 1 Completed](PHASE1_COMPLETED.md) - Implementación del sistema de inteligencia
- [Implementation Plan](implementation_plan.md) - Plan general del proyecto
- [Modelo Inmueble](../../sipi/db/models/inmuebles.py) - Modelo principal
- [Modelo Historial](../../sipi/db/models/historial.py) - Sistema de eventos automáticos

---

## 👤 Autoría

**Implementado por**: Claude Sonnet 4.5
**Fecha**: 2026-01-05
**Sesión**: Arquitectura de Historial de Inmuebles
