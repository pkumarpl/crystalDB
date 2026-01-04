# Multi-stage build for production
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 crystaldb && \
    chown -R crystaldb:crystaldb /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=crystaldb:crystaldb src/ ./src/
COPY --chown=crystaldb:crystaldb scripts/ ./scripts/
COPY --chown=crystaldb:crystaldb data/ ./data/ 2>/dev/null || true
COPY --chown=crystaldb:crystaldb *.csv ./ 2>/dev/null || true

# Create logs directory
RUN mkdir -p logs && chown crystaldb:crystaldb logs

# Switch to non-root user
USER crystaldb

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Run the application
CMD ["python", "-m", "crystaldb.main"]
