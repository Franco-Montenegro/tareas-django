# TaskyPro (Django + DRF)

Gestor de proyectos y tareas estilo mini-Trello. Incluye autenticación, permisos por objeto, filtros, búsqueda y paginación.

## Requisitos
- Python 3.11+
- PostgreSQL 14+
- pip / venv

## Setup rápido
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Completa tus valores
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Endpoints (base /api/)

/projects/, /tasks/, /comments/

Auth de la Browsable API: /api/auth/login/

Tech:

- Django, Django REST Framework, django-filter, PostgreSQL.