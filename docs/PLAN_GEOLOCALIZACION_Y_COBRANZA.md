# Plan de Implementación de Geolocalización y Control de Cobranza

## Análisis de Nomenclatura de la Nueva Aplicación

Dado que la cobranza en microfinanzas es omnicanal (visita en terreno, pago en ventanilla/oficina central, transferencia), el término `field_ops` excluye los pagos in-house. 

Las mejores alternativas para nombrar la nueva aplicación en Django son:

1. **`interactions` (Interacciones):** Es el término más agnóstico y escalable. Un pago en oficina, una llamada telefónica, un SMS de cobranza o una visita física a terreno son, fundamentalmente, "Interacciones con el cliente". Permite englobar la trazabilidad geográfica (si aplica), temporal y el tipo de canal.
2. **`collections` (Cobranza / Recaudación):** Directo a nivel de negocio. Se enfoca estrictamente en el ciclo de recuperación de cartera y sus esfuerzos asociados, sin importar si ocurren en oficina o en la calle.
3. **`tracking` (Seguimiento / Trazabilidad):** Útil si a futuro se piensa auditar no solo al cliente, sino rutas de asesores pasivamente y estados de expedientes.

*Decisión Propuesta para este Plan:* Usar **`interactions`** como núcleo aplicativo. A continuación se detalla la implementación bajo el prefijo `interactions`.

---

## Estrategia de Base de Datos Híbrida (Alineación con TAREAS_PENDIENTES_UID)

Con base en la revisión de políticas arquitectónicas, esta nueva aplicación e integraciones operarán bajo el **Enfoque Híbrido de Llaves Primarias**:
- Las llaves primarias (`id`) de todos los nuevos modelos serán **BigAutoField** para máxima eficiencia en queries y uniones B-Tree internas con `fintech`.
- Se asignará un campo secundario **`uid` (UUIDField)** a aquellos modelos (como `InteractionLog`) que lo requieran para el esquema App Offline/Sincronización (idempotencia y exposición externa en URLs).

---

## Fases de Implementación Arquitectónica

### FASE 1: Fundación del Contexto (`interactions`)
**Objetivo:** Crear la nueva app sin acoplar o romper la lógica contable en `fintech.models`.

1. **Start App:** Ejecutar `python manage.py startapp interactions`.
2. **Modelaje de Geolocalización Planeada (`CollectionPoint`):**
   - Campos: `id` (BigAutoField PK), `uid` (UUIDField), `credit` (FK), `latitude`, `longitude`, `address_type` (Ej. Casa, Oficina Virtual, Ventanilla Sucursal), `is_active`.
   - Propósito: ¿A dónde *creemos* que deberíamos ir o dónde se registró que operaría el crédito?
3. **Modelaje del Registro Inmutable (`InteractionLog`):**
   - Campos: `id` (BigAutoField PK), `uid` (UUIDField clave para Idempotencia), `agent` (FK a Seller/User), `credit` (FK a Credit).
   - Campos de Rastro: `latitude`, `longitude` (al registrar el evento), `timestamp`, `source` (App móvil, Oficina/Dashboard, Importación).
   - Tipos de Interacción: Pago parcial, Pago completo, Promesa de pago, Ausente, Negativa, Llamada.
   - Campos Analíticos: `distance_variance` (Distancia en metros contra el `CollectionPoint`), `offline_sync` (Booleano).

### FASE 2: Integración Transaccional Segura
**Objetivo:** Vincular los esfuerzos de campo (existan cobros o no) a la contabilidad.

1. **Enlace Opcional (`transaction_id`):** `InteractionLog` tendrá una ForeignKey *opcional* (`null=True`) apuntando a `fintech.Transaction`.
   - *Caso A (Pago Efectivo Oficina/Calle):* Guarda GPS y mapea al ID de la transacción contable.
   - *Caso B (Visita fallida):* Guarda GPS, nulo en transacción. (Nos ayuda al KPI de productividad neta).
2. **Override de Model Save / Señales (Signals):** Evitar tocar directamente el monolítico `fintech.models.py`. Suscribir `InteractionLog` para que valide coordenadas lógicamente lícitas.

### FASE 3: Capa de API y Offline-First (Idempotencia)
**Objetivo:** Preparar el backend para que la aplicación móvil soporte desconexión (zonas sin cobertura rural/mercado profundo).

1. **Idempotencia vía UUIDs generados en cliente:** Aprovechando que la tabla `Transaction` y nuestro futuro `InteractionLog` mantuvieron su campo `uid`, el dispositivo móvil del asesor generará el UUID *antes* de enviar la petición. Si se intercepta o hay doble envío al retomar señal, el backend validará por `uid` y evitará crear cobros duplicados.
2. **Endpoints de `interactions`:** 
   - `POST /api/interactions/sync`: Recibe array (Bulk Create) de JSONs con `{uid, lat, lon, datetime, is_offline, transaction_uid}`. NUNCA expone el `id` interno.
3. **Auditoría de Rezagos:** Un cron script calculará la diferencia entre el `timestamp` real de captura del teléfono (guardado sin internet) vs el `created_at` del backend (cuando llegó la señal) para detectar trampas de recaudo.

### FASE 4: Observabilidad en Tableros (Dashboards)
**Objetivo:** Brindar a la dirección general los paneles de control antifraude en tiempo real dentro del módulo `insights` o `revenue`.

1. **Mapa de Calor Diario:** Visualización geoespacial cruzada con estado de cuotas. Puntos verdes (Cobrado en rango de 100mts de recaudo habitual), Puntos rojos (Desviación geográfica severa: posible cobro falso o desviación de ruta).
2. **Métricas de Falsos Productivos:** KPI de Vistas Totales vs Transacciones Efectivas, agrupado por Asesor (Seller).

### FASE 5: Evolución Tecnológica (Próximos Quarter)
1. **Liveness & KYC Identity:** Conectar el `InteractionLog` de firma (Originación) a un motor de biometría que vincule un *selfie* al GPS.
2. **Seguridad End-to-End:** Implementar `django-simple-history` transversal al finalizar el refactoring para la inmutabilidad "Celda por Celda" que requiere una Fintech regulada.
