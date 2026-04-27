# Reporte de Endpoints del Dashboard (Frontend ↔ Backend)

He revisado el código del backend en Django (`apps/dashboard` y `apps/insights`) basándome en tu reporte. Aquí tienes las respuestas a tus consultas para que puedas confirmarlo con el equipo:

### 1. ¿El prefijo es correcto? (`/insights/` vs `/dashboard/`)

**Respuesta:** **Sí, es correcto que tengan prefijos diferentes.**
En el backend de Django, existen dos aplicaciones distintas:
- `apps/insights/`: Maneja los dashboards principales y analíticas. Todas sus rutas están agrupadas bajo el prefijo `/insights/`.
- `apps/dashboard/`: Es una aplicación separada que, entre otras cosas, maneja los datos para los gráficos (`SellerChartDataAPIView` y `MonthlyChartDataAPIView`). Sus rutas están agrupadas bajo el prefijo `/dashboard/`.

Por lo tanto, la estructura actual que están llamando desde el frontend es correcta con respecto a cómo está construido el backend.

---

### 2. ¿Parámetro `seller` o `seller_id`?

**Respuesta:** **El frontend lo está enviando correctamente según lo que el backend espera en cada caso, aunque el backend es inconsistente.**

Al revisar el código de las vistas (`views.py` en ambas apps), esto es lo que espera el backend:

- **Endpoints de Gráficos (`/dashboard/...`)**: El backend busca explícitamente `seller_id` en el body del request.
  ```python
  # En apps/dashboard/views.py
  seller_id = request.data.get("seller_id")
  ```

- **Endpoints de Insights (`/insights/...`)**: La mayoría de las vistas están configuradas para leer `seller` de los query params.
  ```python
  # En apps/insights/views.py (ej. ExecutiveDashboardView, CreditAnalyticsView)
  seller_id = request.query_params.get('seller')
  ```

- **Nota sobre el endpoint de la tabla (`/insights/credits/table/`)**: Este endpoint específico busca `seller_id` en los query params, a diferencia del resto de la app `insights`.
  ```python
  'seller_id': request.query_params.get('seller_id')
  ```

- **Nota sobre `/insights/credits/analytics/`**: Esta vista está preparada para aceptar cualquiera de los dos identificadores.
  ```python
  seller_id = request.query_params.get('seller_id') or request.query_params.get('seller')
  ```

**Conclusión:** Continúa enviando `seller` para los dashboards principales y `seller_id` para los gráficos y la tabla de créditos.

---

### 3. Endpoints Nuevos: ¿Existen ya los endpoints `/insights/credits/analytics/` y `/insights/risk/analysis/`?

**Respuesta:** **Sí, los endpoints ya existen en el código del backend.**

Están mapeados en el archivo `apps/insights/urls.py` de la siguiente manera:
```python
path('credits/analytics/', views.CreditAnalyticsAdvancedView.as_view(), name='credits_analytics_advanced'),
path('risk/analysis/', views.RiskAnalysisAdvancedView.as_view(), name='risk_analysis_advanced'),
```

**Si estás recibiendo un Error 404, revisa lo siguiente:**
1. **Trailing Slashes (`/`)**: Django por defecto exige que las URLs terminen con una barra invertida `/`. Asegúrate de que el frontend está llamando a `/insights/credits/analytics/` (con slash al final) y NO a `/insights/credits/analytics`.
2. **Configuración de Proxy**: Si estás usando un proxy en Next.js (por ejemplo en `next.config.js` o `rewrites`), verifica que estas nuevas rutas de `/insights/*` estén bien configuradas para apuntar al servidor backend.
3. **Despliegue/Entorno**: Asegúrate de que el backend local o el servidor al que estás apuntando esté corriendo la última rama de código que incluye estas vistas nuevas.
