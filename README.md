# 🧑‍💼 Ducky Ways – Proyecto Django

Este proyecto es una versión simplificada de LinkedIn, desarrollada con Django. Permite la gestión de ofertas de trabajo, candidaturas, agendas de entrevistas y comunicación entre headhunters y candidatos.

---

## 🚀 Funcionalidades principales

- Autenticación de usuarios con roles (`headhunter` y `candidato`)
- Panel de control personalizado para cada tipo de usuario
- Gestión de ofertas de trabajo (`JobOffer`)
- Aplicación a ofertas mediante candidaturas (`Candidatura`)
- Agenda semanal con eventos tipo entrevista, llamada, entrega, etc.
- Envío automático de correos al cambiar el estado de una candidatura
- Interfaz visual con Bootstrap y FullCalendar

---

## 🛠️ ¿Qué hemos hecho con Django?

- Creación del proyecto Django y la app principal `jobs`
- Definición de modelos personalizados para ofertas, candidaturas y acciones de agenda
- Uso de vistas basadas en clases (`ListView`, `TemplateView`) y decoradores personalizados para controlar el acceso según el rol
- Implementación de formularios dinámicos para actualizar el estado de las candidaturas
- Integración del envío de correos usando `send_mail()` desde el backend
- - **Modificación del template `base.html` para personalizar la barra de navegación (`navbar`) según el rol del usuario autenticado**:
  - Se muestran enlaces específicos dependiendo de si el usuario es `headhunter` o `candidato`
  - Se ocultan opciones irrelevantes para cada tipo de usuario, mejorando la claridad y usabilidad
  - Se incluye lógica condicional en el template para mostrar el enlace de cierre de sesión y otras funcionalidades contextuales

---

## ⚙️ Modificaciones en `settings.py`

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@opentojob.es'

LOGIN_REDIRECT_URL = '/'

INSTALLED_APPS += [
    'crispy_forms',
    'jobs',
]

STATICFILES_DIRS = [BASE_DIR / "static"]

