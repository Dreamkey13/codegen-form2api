# Use Python 3.9 as base image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN wget -qO- https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements files
COPY requirements.txt .
COPY requirements-dev.txt .
COPY ui/package*.json ./ui/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js dependencies
RUN cd ui && npm install

# Copy application code
COPY . .

# Install Playwright browsers
RUN playwright install chromium

# Build React UI
RUN cd ui && npm run build

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV PYTHONPATH=/app
ENV NODE_ENV=production

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Start the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"] 