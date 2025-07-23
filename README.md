
# DuckyProject

Un foro de preguntas y respuestas basado en Django, donde los usuarios pueden hacer preguntas al público o a profesionales de manera privada según el sector.

## Funcionalidades
- Autenticación de usuarios  
- Preguntas públicas y privadas  
- Profesionales filtrados por sector  
- Foro con respuestas y moderación  

## Inicio Rápido
1. Clona el repositorio.  
2. Instala las dependencias:
   ```bash
   pip install django python-decouple python-dirtyfields
   ```
3. Aplica las migraciones:
   ```bash
   python manage.py migrate
   ```
4. Ejecuta el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```
5. Accede a la aplicación en `http://127.0.0.1:8000/`

## Estructura de Carpetas
- `account/` - Gestión de cuentas de usuario  
- `forum/` - Aplicación del foro (preguntas, respuestas, profesionales)  
- `core/` - Utilidades principales  
- `config/` - Configuraciones del proyecto Django  
- `templates/` - Plantillas HTML  
- `static/` - Archivos estáticos (CSS, imágenes)  

## Notas
- Para hacer una pregunta privada, selecciona primero un sector y luego elige un profesional de ese sector.  
- Para desarrollo, puedes usar la base de datos SQLite por defecto o configurar la tuya propia en `config/settings.py`.

---
Licencia MIT
```
