# =========================
# Base Image
# =========================
FROM python:3.10-slim

# =========================
# Environment settings
# =========================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# =========================
# Working directory
# =========================
WORKDIR /app

# =========================
# System dependencies
# =========================
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Install Python dependencies
# =========================
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =========================
# Copy project files
# =========================
COPY . .

# =========================
# Expose Flask port
# =========================
EXPOSE 5000

# =========================
# Start command
# =========================
CMD ["python", "app.py"]
