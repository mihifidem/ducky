# 🦆 Ducky - Sistema de Gestión de Currículums

Ducky es una aplicación web desarrollada en Django que permite gestionar currículums de usuarios, generar versiones en PDF con diferentes estilos y exportarlos de forma masiva en un archivo `.zip`. Es una herramienta pensada para facilitar la organización y presentación de perfiles profesionales.

---

## 📚 Índice

- [🦆 Ducky - Sistema de Gestión de Currículums](#-ducky---sistema-de-gestión-de-currículums)
  - [📚 Índice](#-índice)
  - [📦 Manual de instalación](#-manual-de-instalación)
    - [Requisitos previos](#requisitos-previos)
    - [Pasos de instalación](#pasos-de-instalación)
  - [🛠 Tecnologías usadas](#-tecnologías-usadas)
  - [👨‍💻 Manual de usuario básico](#-manual-de-usuario-básico)
    - [Acceso al sistema](#acceso-al-sistema)
    - [Funcionalidades principales](#funcionalidades-principales)
  - [📁 Estructura del proyecto](#-estructura-del-proyecto)
  - [📄 Licencia](#-licencia)
  - [✨ Créditos](#-créditos)

---

## 📦 Manual de instalación

### Requisitos previos

- Python 3.10 o superior  
- SQLite (incluido por defecto en Python)

### Pasos de instalación

1. **Clonar el repositorio:**

```bash
git clone https://github.com/mihifidem/ducky
cd ducky
```

2. **Crear entorno virtual y activarlo:**

```bash
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

4. **Aplicar migraciones:**

```bash
python manage.py migrate
```

5. **Crear superusuario (opcional):**

```bash
python manage.py createsuperuser
```

6. **Ejecutar servidor:**

```bash
python manage.py runserver
```

---

## 🛠 Tecnologías usadas

- **Backend:**  
  - Django  
  - SQLite (base de datos por defecto)

- **Frontend:**  
  - Bootstrap (interfaz responsive)

- **Otras bibliotecas y herramientas:**  
  - Pillow (procesamiento de imágenes)  
  - Xhtml2pdf (generación de currículums en PDF)  
  - zipfile (para exportación de múltiples PDFs)

---

## 👨‍💻 Manual de usuario básico

### Acceso al sistema

1. Inicia el servidor con `python manage.py runserver`  
2. Accede a `http://127.0.0.1:8000/` desde tu navegador  
3. Inicia sesión o regístrate si la aplicación lo permite

### Funcionalidades principales

- Gestión de usuarios y perfiles profesionales  
- Carga de información personal y laboral  
- Generación de currículums en formato PDF  
- Elección de estilo de presentación para cada currículum  
- Exportación masiva de currículums en un archivo `.zip`  
- Acceso a panel administrativo (`/admin`) para gestión avanzada  
- Gestión de error 404 (página no encontrada)
---

## 📁 Estructura del proyecto

```
ducky-main
├───account
│   └───templates
│       └───account
│           └───skins
│               └───pdf
├───config
├───core
│   └───templates
│       └───core
├───media
│   ├───avatars
│   └───cv_zips
├───static
│   ├───css
│   ├───img
│   └───js
└───templates
    └───cv
```
---

## 📄 Licencia

Este proyecto se distribuye bajo una licencia privada o libre, según corresponda. Puedes especificarla aquí.

---

## ✨ Créditos

Desarrollado por el equipo de ***Ducky CV*** 🦆:
- David Gutierrez Ramos
- Santiago Henao Salazar
- Jordi Martin Pulido
- Daniel Punti Prats
