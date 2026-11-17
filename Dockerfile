FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project source
COPY . .

# Ensure runtime directories exist
RUN mkdir -p /app/data /app/core/media/profile_pictures /app/staticfiles

# Collect static files into image
RUN python manage.py collectstatic --noinput

# Expose Gunicorn port
EXPOSE 5005

# Run migrations, sync static files to volume, and start Gunicorn
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn --config gunicorn-cfg.py core.wsgi"]
