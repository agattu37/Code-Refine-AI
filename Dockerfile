FROM python:3.11-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update \
    && apt-get install -y build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only pyproject/poetry lock first to leverage layer caching
COPY backend/pyproject.toml backend/poetry.lock ./

# Install poetry and project dependencies
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy application code
COPY backend/ ./backend/

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Use PORT provided by the hosting environment (Render sets $PORT)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
