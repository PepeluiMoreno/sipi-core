# Arquitectura del Historial de Inmuebles - Decisión Arquitectónica

**Fecha**: 2026-01-05
**Estado**: ✅ IMPLEMENTADO

---

## 📋 Resumen Ejecutivo

Se ha decidido **NO implementar un sistema genérico de procesos** con meta-información configurable. En su lugar, se utilizan **3 modelos específicos** que ya existen en la aplicación, complementados con una **propiedad computada** en el modelo `Inmueble` para generar un timeline unificado.

---

## 🎯 Contexto

### Opción Descartada: Sistema Genérico de Procesos

Se diseñó inicialmente un sistema complejo con:
- `TipoProceso`, `TipoActor`, `ProcesoInmueble`, `ProcesoActor`, `ProcesoDocumento`
- Tablas de configuración: `ProcesoTipoActorRequerido`, `ProcesoTipoDocumentoRequerido`
- Script de población: `populate_proceso_config.py`
- 6+ tablas adicionales para meta-información

**Objetivo**: Configurar dinámicamente qué actores y documentos requiere cada tipo de proceso.

### Razones para Descartarlo

1. **Sobrecomplica innecesariamente**: Ya existen 3 modelos específicos que funcionan perfectamente
2. **No hay requisito real de extensibilidad**: Solo hay 3 tipos de procesos previstos
3. **Añade indirección**: Polimorfismo, lookups dinámicos, más difícil de mantener
4. **Duplicación de lógica**: Los modelos específicos ya tienen todos los campos necesarios

---

## ✅ Solución Implementada: Modelos Específicos + Timeline

### 1. Tres Modelos Específicos (Ya existentes)

#### `Inmatriculacion` ([inmuebles.py:120-138](../../src/sipi/db/models/inmuebles.py#L120-L138))
Registro inicial de propiedad en el Registro de la Propiedad.

**Campos clave**:
- `fecha_inmatriculacion`
- `numero_finca`, `tomo`, `libro`, `folio`, `inscripcion`
- `registro_propiedad_id` (FK a RegistroPropiedad)
- `tipo_certificacion_propiedad_id` (FK a TipoCertificacionPropiedad)

**Relación**: `Inmueble.inmatriculaciones`

---

#### `Transmision` ([transmisiones.py:12-39](../../src/sipi/db/models/transmisiones.py#L12-L39))
Compraventas y transferencias de propiedad.

**Campos clave**:
- `fecha_transmision`
- `precio_venta`
- `notaria_id` (FK a Notaria)
- `registro_propiedad_id` (FK a RegistroPropiedad)
- `tipo_transmision_id` (FK a TipoTransmision)
- `tipo_certificacion_propiedad_id`

**Actores relacionados**:
- Transmitente (TODO: modelar vía `Privado`)
- Adquiriente (TODO: modelar vía `Privado`)
- Notaria
- RegistroPropiedad
- AgenciaInmobiliaria (vía `TransmisionAnunciante`)

**Relación**: `Inmueble.transmisiones`

---

#### `Actuacion` ([actuaciones.py:11-31](../../src/sipi/db/models/actuaciones.py#L11-L31))
Intervenciones físicas sobre el inmueble (rehabilitaciones, restauraciones).

**Campos clave**:
- `nombre`, `descripcion`
- `fecha_inicio`, `fecha_fin`
- `presupuesto`

**Actores relacionados**:
- Técnicos (vía `ActuacionTecnico` con roles: arquitecto, aparejador, etc.)
- Administraciones (vía `ActuacionSubvencion`)

**Relación**: `Inmueble.actuaciones`

---

### 2. Propiedad Computada: `timeline_procesos`

**Ubicación**: [inmuebles.py:119-177](../../src/sipi/db/models/inmuebles.py#L119-L177)

**Propósito**: Generar un timeline unificado de todos los procesos que han afectado al inmueble.

**Implementación**:
```python
@property
def timeline_procesos(self) -> List[dict]:
    """
    Retorna todos los procesos del inmueble ordenados cronológicamente.

    Incluye: Inmatriculaciones, Transmisiones y Actuaciones.
    Cada entrada contiene: tipo, fecha, id, y datos relevantes del proceso.

    Returns:
        List[dict]: Lista de eventos ordenados por fecha (más reciente primero)
    """
    eventos = []

    # Inmatriculaciones
    for inmat in self.inmatriculaciones:
        eventos.append({
            'tipo': 'INMATRICULACION',
            'fecha': inmat.fecha_inmatriculacion,
            'id': inmat.id,
            'numero_finca': inmat.numero_finca,
            'registro_propiedad_id': inmat.registro_propiedad_id,
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

    # Ordenar por fecha (más reciente primero)
    return sorted(eventos, key=lambda x: x['fecha'] or x['created_at'], reverse=True)
```

**Uso desde GraphQL**:
```graphql
query TimelineInmueble($id: ID!) {
  inmueble(id: $id) {
    id
    nombre
    timeline_procesos {
      tipo
      fecha
      id
      ... # campos específicos según tipo
    }
  }
}
```

---

## 🔄 Sistema de Inteligencia (Historial del Inmueble)

**Separado de los procesos formales**, el sistema de inteligencia usa `EventoHistorial` para **detectar automáticamente eventos** desde fuentes externas y registrarlos en el Historial/bitácora del inmueble.

### Modelo: `EventoHistorial` ([Historial.py:27-56](../../src/sipi/db/models/Historial.py#L27-L56))

**Propósito**: Historial digital del inmueble que traza eventos detectados automáticamente por scrapers y ETL.

**Tipos de eventos** (`TipoEventoHistorial`):
- `ALTA_INMATRICULACION` - Detectado en scraper de BOE
- `PUESTA_EN_VENTA` - Detectado en portales inmobiliarios
- `VENDIDO` - Detectado por cambio de estado en portales
- `REHABILITACION` - Detectado en contratación pública
- `REHABILITACION_SUBVENCIONADA` - Detectado en BDNS
- `DECLARACION_BIC` - Detectado en boletines oficiales
- `CAMBIO_VISITABILIDAD` - Detectado en webs de turismo

**Campos**:
- `tipo_evento` (ENUM)
- `fecha_evento`
- `detalles` (JSONB) - Datos estructurados del evento
- `descripcion` (Text) - Descripción legible
- `fuente` (String) - Origen: "Scraper-Idealista", "Scraper-BOE", etc.

**Relación**: `Inmueble.Historial`

### Diferencia clave: Procesos vs Historial

| Aspecto | Procesos (Inmatriculacion, Transmision, Actuacion) | Historial |
|---------|-----------------------------------------------------|------------|
| **Origen** | Ingreso manual por usuarios | Detección automática por scrapers |
| **Formalidad** | Procesos formales con documentación | Eventos informativos/señales |
| **Actores** | Relaciones FK a actores específicos | Solo metadatos en JSON |
| **Propósito** | Registro oficial del inmueble | Inteligencia/vigilancia |
| **Ejemplo** | Escritura de compraventa registrada | Anuncio de venta detectado en Idealista |

---

## 📊 Comparativa de Enfoques

| Aspecto | Sistema Genérico (descartado) | Modelos Específicos (implementado) |
|---------|-------------------------------|-------------------------------------|
| **Complejidad** | 6+ tablas, polimorfismo, meta-info | 3 modelos directos + 1 propiedad |
| **Type Safety** | Campos dinámicos (JSONB) | Campos tipados en modelos |
| **Queries** | Joins complejos, lookups dinámicos | Relaciones directas SQLAlchemy |
| **Mantenibilidad** | Configuración en BD + código | Solo código (modelos) |
| **Extensibilidad** | Añadir en configuración | Crear nuevo modelo específico |
| **Documentos** | Sistema de meta-información | Relaciones directas a `Documento` |

**Conclusión**: Para 3 tipos de procesos bien definidos, modelos específicos son más simples, mantenibles y type-safe.

---

## 🚀 Próximos Pasos

### Inmediatos
1. ✅ Implementar `timeline_procesos` en `Inmueble`
2. ✅ Agregar relación `Historial` a `Inmueble`
3. ✅ Renombrar `InmuebleLifecycle` → `EventoHistorial` (terminología más española)
4. ✅ Eliminar archivos del sistema genérico
5. ⏳ Crear migración Alembic para renombrar tabla `inmueble_lifecycle` → `Historial_inmueble`

### Mejoras Futuras
1. **Estado de Documentación**: Agregar propiedad computada `estado_documentacion` a cada modelo específico
   ```python
   @property
   def estado_documentacion(self) -> str:
       # DOCUMENTADO | PARCIALMENTE_DOCUMENTADO | NO_DOCUMENTADO
       # Basado en presencia de documentos relacionados
   ```

2. **Timeline Unificado en Frontend**: UI que muestre tanto `timeline_procesos` como `Historial` en un solo timeline visual

3. **GraphQL Types**: Auto-generar tipos GraphQL para `timeline_procesos` usando Strawberry unions:
   ```python
   @strawberry.type
   class TimelineEventoInmatriculacion:
       tipo: str
       fecha: datetime
       numero_finca: str
       ...

   TimelineEvento = Annotated[
       Union[TimelineEventoInmatriculacion, TimelineEventoTransmision, TimelineEventoActuacion],
       strawberry.union("TimelineEvento")
   ]
   ```

---

## 📁 Archivos Modificados

```
sipi-core/
├── src/sipi/db/models/
│   ├── inmuebles.py         [MODIFICADO] - Agregada propiedad timeline_procesos y relación Historial
│   ├── __init__.py          [MODIFICADO] - Exportar EventoHistorial y TipoEventoHistorial
│   ├── transmisiones.py     [SIN CAMBIOS] - Modelo ya existente
│   ├── actuaciones.py       [SIN CAMBIOS] - Modelo ya existente
│   ├── Historial.py        [NUEVO] - Modelo EventoHistorial (renombrado desde lifecycle.py)
│   └── lifecycle.py         [ELIMINADO] - Renombrado a Historial.py
│
├── docs/agent_handoff/
│   ├── ARQUITECTURA_PROCESOS.md      [NUEVO] - Este documento
│   ├── README.md                      [MODIFICADO] - Actualizado estado del proyecto
│   ├── PHASE1_COMPLETED.md            [MODIFICADO] - Actualizado nombres de modelos
│   ├── MODELO_PROCESOS_REDESIGN.md    [ELIMINADO]
│   ├── UI_PROCESOS_DOCUMENTACION.md   [ELIMINADO]
│   └── CLARIFICATION_DOCUMENTOS.md    [ELIMINADO]
│
└── scripts/
    └── populate_proceso_config.py [ELIMINADO]
```

---

## 💡 Lecciones Aprendidas

1. **KISS (Keep It Simple)**: No sobre-diseñar cuando modelos específicos son suficientes
2. **YAGNI (You Aren't Gonna Need It)**: No implementar extensibilidad genérica sin requisito claro
3. **Type Safety > Flexibilidad**: En aplicaciones empresariales, preferir tipos explícitos sobre configuración dinámica
4. **Separation of Concerns**: Separar procesos formales (Inmatriculacion, Transmision, Actuacion) de eventos de inteligencia (LifecycleEvents)

---

## 📚 Referencias

- [Phase 1 Completed](PHASE1_COMPLETED.md) - Implementación del sistema de inteligencia
- [Implementation Plan](implementation_plan.md) - Plan general del proyecto
- [Modelos de Inmuebles](../../src/sipi/db/models/inmuebles.py)
- [Modelos de Transmisiones](../../src/sipi/db/models/transmisiones.py)
- [Modelos de Actuaciones](../../src/sipi/db/models/actuaciones.py)
- [Historial del Inmueble](../../src/sipi/db/models/Historial.py)
