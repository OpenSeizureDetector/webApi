# Use official Python image as a base
FROM python:3.11

# Set working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies first (for better caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code into the container
COPY webApi ./webApi

# Copy manage.py and any other root files needed for startup
COPY manage.py ./

# Expose port (matches docker-compose.yml)
EXPOSE 8000

# Set environment variable for Django settings module
ENV DJANGO_SETTINGS_MODULE=webApi.settings

# Default command to run Django development server (override in docker-compose if needed)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]