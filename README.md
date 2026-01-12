# Teacher Portfolio (Django)
[![Django CI](https://github.com/ncoliver/teacherpf-ubuntuws/actions/workflows/django.yml/badge.svg)](https://github.com/ncoliver/teacherpf-ubuntuws/actions/workflows/django.yml)
## Concept
Artifacts are organized by **School Year** (e.g. 2025-2026) and **Category**:
- Activities
- Coding Activities
- Presentations
- Projects

Each artifact has:
- title, description
- linked standards
- images
- videos (URL or uploaded file)

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
