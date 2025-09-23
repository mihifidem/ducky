# 🌐 Mapa de navegación por rol

## HOME (/)
- **Visibilidad:** Todos
- **Contenido:** Listado de tests disponibles
- **Acciones:**
  - **Alumno** → Hacer test → `/management_test/test/<filename>/`
  - **Profesor** → Modificar test → `/management_test/modificar/<filename>/`
  - **Profesor** → Crear test → `/management_test/crear-test/` (botón visible solo para teacher)

---

## ALUMNO (rol='alumno')
- **Dashboard** → `/dashboard/alumno/`  
  - Estadísticas personales: aciertos/fallos, gráficos por categoría
- **Historial de tests** → `/management_test/mis-resultados/`  
  - Listado de tests realizados con detalles
- **Realizar test** → `/management_test/test/<filename>/`  
  - Seleccionar categoría (solo tests de inteligencias múltiples) → `/management_test/seleccionar_categorias/<filename>/`
- **Responder comentario** → `/comentarios/<resultado_id>/responder/`

---

## PROFESOR (rol='teacher')
- **Dashboard** → `/dashboard/profesor/`  
  - Estadísticas agregadas por estudiantes, gráficos, filtros
- **Crear test** → `/management_test/crear-test/`
- **Modificar test** → `/management_test/modificar/<filename>/`  
  - Modificar test de inteligencias múltiples → `/management_test/modificar_inteligencias/<filename>/`
- **Dejar comentarios sobre resultados** → `/comentarios/<resultado_id>/`

---

## ADMIN / SUPERUSER
- **Dashboard** → `/dashboard/admin/`  
  - Estadísticas globales, comparativas, gráficos
- **Crear test** → `/management_test/crear-test/`
- **Modificar test** → `/management_test/modificar/<filename>/`
- **Estadísticas globales** → `/estadisticas/globales/`

---

## RESULTADOS DE TEST
- **Vista resultado** → `/management_test/resultado/<resultado_id>/`
- **Exportar PDF** → `/management_test/resultado/<resultado_id>/pdf/`  
  - Requiere plantilla: `templates/management_test/resultado_pdf.html`

---

## 📌 Decoradores de acceso sugeridos

| Vista | Decorador |
|-------|-----------|
| Tests (hacer, seleccionar categorías, resultado) | `@login_required` |
| Crear/Modificar tests | `@login_required + @user_passes_test(lambda u: u.rol=='teacher')` |
| Dashboard alumno | `@login_required + @user_passes_test(lambda u: u.rol=='alumno')` |
| Dashboard profesor | `@login_required + @user_passes_test(lambda u: u.rol=='teacher')` |
| Dashboard admin | `@login_required + @user_passes_test(lambda u: u.is_superuser)` |

---

## 🛠 Endpoints clave para la API futura

- `/api/tests/` → listar todos los tests  
- `/api/tests/<id>/` → detalle de test  
- `/api/tests/crear/` → crear test (teacher/admin)  
- `/api/tests/<id>/modificar/` → modificar test  
- `/api/tests/<id>/respuestas/` → enviar respuestas (alumno)  
- `/api/resultados/<id>/` → ver resultado (alumno/profesor)  
- `/api/comentarios/<id>/` → listar/comentar resultados

# ✅ Plan de Sprints con estado

## 🟢 SPRINT 1 (60h): Fundamentos del sistema + ejecución de tests

| Nº   | Tarea                                         | Estado       |
|------|-----------------------------------------------|--------------|
| T1   | Cargar y mostrar lista de tests desde archivos JSON | ✅ Hecho |
| T2   | Realizar tests clásicos (pregunta a pregunta) | ✅ Hecho |
| T3   | Guardar resultados de test clásico            | ✅ Hecho |
| T4   | Mostrar resumen del test con aciertos/fallos  | ✅ Hecho |
| T6   | Historial de tests del usuario                | ✅ Hecho |
| T24  | Controlar navegación entre preguntas          | ✅ Hecho |
| T25  | Barra de progreso del test                    | ✅ Hecho |
| T27  | Gestión de errores al cargar JSON             | ✅ Hecho |
| T28  | Reiniciar test si ya fue iniciado             | ✅ Hecho |

**Total Sprint 1:** casi completo (falta solo validación/errores al cargar JSON).

---

## 🟡 SPRINT 2 (60h): Inteligencias múltiples + dashboards

| Nº   | Tarea                                         | Estado       |
|------|-----------------------------------------------|--------------|
| T4   | Realizar test de inteligencias múltiples      | ✅ Hecho |
| T5   | Guardar resultados + cálculo por categorías   | ✅ Hecho |
| T7   | Dashboard del alumno con métricas             | 🟡 Parcial (ya muestra resultados, falta mejorar gráficos) |
| T8   | Dashboard del profesor                        | 🟡 Parcial (filtros y métricas por alumno aún básicos) |
| T9   | Añadir comentarios de profesor                | ✅ Hecho |
| T10  | Modificar comentarios de profesor             | ✅ Hecho |
| T11  | Indicar si un resultado tiene comentario      | ✅ Hecho |
| T22  | Comentario del alumno                         | ✅ Hecho |
| T12  | Acceso restringido por grupo                  | ✅ Hecho (rol + user_passes_test) |
| T26  | Validación de test mínimo preguntas           | 🔴 Pendiente |
| T21  | Filtrado de resultados por test               | 🟡 Parcial |

**Total Sprint 2:** Avanzado, pero aún con pendientes (validaciones y dashboards más completos).

---

## 🟡 SPRINT 3 (60h): Edición y creación de tests

| Nº   | Tarea                                         | Estado       |
|------|-----------------------------------------------|--------------|
| T13  | Crear test desde formulario y guardar JSON    | ✅ Hecho |
| T14  | Editar test clásico desde JSON                | ✅ Hecho |
| T15  | Editar test de inteligencias múltiples        | ✅ Hecho |
| T16  | Gestión de categorías y subcategorías         | 🟡 Parcial |
| T17  | Etiquetas (tags) por test                     | 🔴 Pendiente |
| T18  | Gráfico de resultados por pregunta            | 🟡 Parcial (puede hacerse con Chart.js) |
| T19  | Gráfico de aciertos por categoría             | 🟡 Parcial |
| T20  | Dashboard visual para alumno (KPIs, evolución)| 🟡 Parcial |
| T23  | Vincular preguntas a categoría en backend     | 🟡 Parcial |
| T29  | Mejora visual y estilo uniforme de forms      | 🟡 En progreso |
| T30  | Añadir mensajes de éxito/error                | ✅ Hecho (ya usas messages en algunas vistas) |

**Total Sprint 3:** La edición de tests está lista ✅, pero faltan gráficos, mejoras visuales y categorías completas.

---

## 🔴 SPRINT 4 (60h): Mejoras UX + robustez + visualización

| Nº   | Tarea                                         | Estado       |
|------|-----------------------------------------------|--------------|
| T31  | Vista de resumen gráfico en dashboard profesor| 🔴 Pendiente |
| T32  | Ranking de alumnos por aciertos               | 🔴 Pendiente |
| T33  | Evolución de un usuario en gráficos de línea  | 🔴 Pendiente |
| T34  | Exportación de resultados a CSV               | 🔴 Pendiente |
| T35  | Buscador por título o usuario                 | 🔴 Pendiente |
| T36  | Validar existencia de archivo JSON            | 🔴 Pendiente |
| T37  | Añadir breadcrumbs y navegación amigable      | 🔴 Pendiente |
| T38  | Validación de datos en formularios            | 🔴 Pendiente |
| T39  | Añadir tests automáticos (pytest)             | 🔴 Pendiente |
| T40  | Documentar código y endpoints                 | 🟡 Parcial |
| T41  | Preparar entrega (limpieza BBDD)              | 🔴 Pendiente |
| T42  | Ayuda contextual en vistas                    | 🔴 Pendiente |

**Total Sprint 4:** Todavía no iniciado, salvo algo de documentación.

---

## 📊 Resumen del avance

- **Sprint 1:** ✅ Completo al 100%  
- **Sprint 2:** 🟡 Avanzado (~70%)  
- **Sprint 3:** 🟡 Avanzado (~60%)  
- **Sprint 4:** 🔴 No iniciado  
