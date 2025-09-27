# Sprint - Gestión de Ofertas y Candidaturas

Este sprint incluye la creación de modelos y funcionalidades relacionadas con ofertas de trabajo, candidaturas y gestión de roles en el sistema.

---

## 📌 Tareas del Sprint

### ✅ T1 - Modelo **JobOffer**
Se creó el modelo `JobOffer` con los siguientes campos:
- `título`
- `descripción`
- `salario`
- `modalidad`
- `ubicación`
- `beneficios`
- Otros campos relacionados

Además:
- Se configuró la clase `Meta`.
- Se implementó el método `__str__`.

---

### ✅ T2 - Modelo **Candidatura**
Se creó el modelo `Candidatura`, el cual relaciona a `User` con `JobOffer`.

Campos añadidos:
- `estado` (con **choices**)
- `mensaje_personalizado`
- `fecha_de_aplicación`
- Configuración de `verbose_name`

---

### ✅ T4 - Modelo **StatusMessageTemplate**
Se creó el modelo `StatusMessageTemplate` para que los **headhunter** puedan guardar mensajes tipo según el estado de la candidatura.

Campos:
- `user`
- `estado`
- `mensaje`

---

### ✅ T6 - Decoradores y Mixins para roles
Se implementaron decoradores y mixins para control de acceso:
- `headhunter_required`
- `role_required`
- `HeadhunterRequiredMixin`

Aplicables tanto en vistas basadas en funciones como en clases.

---

### ✅ T15 - Grupos en Django Admin
Se configuraron grupos de usuarios en **Django Admin**:
- `candidate`
- `headhunter`

Además, se verificó la asignación de grupos tras **login/registro**.

---

## 🔎 Revisión del Sprint
- Los modelos se encontraban correctamente creados.  
- Se regeneró la base de datos.  
- Desde el **Django Admin**, se completó la **Tarea 15** de gestión de grupos.  

---