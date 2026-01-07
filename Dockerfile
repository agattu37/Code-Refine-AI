FROM python:3.11-slim

WORKDIR /app

# Install build dependencies needed for many Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       curl \
       gcc \
       libffi-dev \
       libssl-dev \
       python3-dev \
       pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install via pip
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy application code
COPY backend/ ./backend/

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Use PORT provided by the hosting environment (Render sets $PORT)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

# Bump: updated to ensure Render picks up latest Dockerfile (timestamp)
# Timestamp: 2026-01-06
