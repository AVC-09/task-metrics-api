# Stage 1: Builder stage (compiles dependencies)
FROM python:3.11-slim AS builder

WORKDIR /app

# Layer Caching Optimization: Copy requirements first to cache dependency layers
COPY requirements.txt .

# Install dependencies into the user local directory (/root/.local)
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final runtime stage (minimal image)
FROM python:3.11-slim AS runner

WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /root/.local /root/.local

# Copy app code
COPY main.py .

# Update PATH so the system finds the installed packages
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Expose FastAPI default port
EXPOSE 8000

# Run Uvicorn server binding to 0.0.0.0
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]