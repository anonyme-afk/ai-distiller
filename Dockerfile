FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY config/ config/
COPY .env.example .env.example

# Set python path
ENV PYTHONPATH=/app/src

# Default command (can be overridden by docker-compose)
CMD ["uvicorn", "ai_distiller.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
