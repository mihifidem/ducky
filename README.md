# DuckyProject

Un foro de pregunta y respuesta basado en Django donde usuarios pueden preguntar al publico o a profesionales de manera privada depende del sector.

## Features
- User authentication
- Public and private questions
- Professionals filtered by sector
- Forum with answers and moderation

## Quick Start
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```
5. Access the app at `http://127.0.0.1:8000/`

## Folder Structure
- `account/` - User account management
- `forum/` - Forum app (questions, answers, professionals)
- `core/` - Core utilities
- `config/` - Django project settings
- `templates/` - HTML templates
- `static/` - Static files (CSS, images)

## Notes
- To ask a private question, select a sector first, then choose a professional from that sector.
- For development, use the default SQLite database or configure your own in `config/settings.py`.

---
MIT License
