FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (add others if you need pillow, psycopg, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Install python deps first for better layer caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -U pip wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create directories for static/media (optional but common)
RUN mkdir -p /app/staticfiles /app/media

# Default Gunicorn command (replace `myproject` with your Django project module)
CMD ["gunicorn", "teacherportfolio.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
