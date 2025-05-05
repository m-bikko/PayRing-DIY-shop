FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy application code
COPY . .

# Create directory structure and set permissions
RUN mkdir -p /app/instance && \
    chmod 777 /app/instance

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Run gunicorn
CMD gunicorn --bind 0.0.0.0:8080 "app:create_app()"