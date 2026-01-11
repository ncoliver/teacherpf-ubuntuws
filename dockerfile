# =========================
# Option A: Django 6.x  ✅  (Python 3.12+ required)
# File: Dockerfile
# =========================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /teacherpf-ubuntuws

# Some deps (cryptography/cffi) may compile on some architectures; Rust needed if no wheel. :contentReference[oaicite:3]{index=3}
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    libssl-dev \
    libffi-dev \
    rustc \
    cargo \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /teacherpf-ubuntuws/requirements.txt

RUN python -m pip install --upgrade pip setuptools wheel \
 && python -m pip install --retries 10 --timeout 120 -r /app/requirements.txt

COPY . /teacherpf-ubuntuws

EXPOSE 8000
CMD ["gunicorn", "  teacherportfolio.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "60"]


# =========================
# Option B: Stay on Python 3.11 ✅ (Downgrade Django)
# 1) Change base image to python:3.11-slim
# 2) Change requirements: Django==5.2.10 (or latest 5.2.x)
# =========================
# FROM python:3.11-slim
# ...
# requirements.txt change:
#   Django==5.2.10
