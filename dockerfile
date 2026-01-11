# File: Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /teacherpf-ubuntu

# Keep this minimal; add libs only if your requirements need them.
# build-essential: needed when any dependency compiles native extensions.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip setuptools wheel \
 && python -m pip install --retries 10 --timeout 120 -r /app/requirements.txt

COPY . /teacherpf-ubuntu

EXPOSE 8000

# Replace with your actual module path
CMD ["gunicorn", "teacherportfolio.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "60"]
