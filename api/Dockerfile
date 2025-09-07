FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
	apt-get install -y --no-install-recommends \
		build-essential \
		default-libmysqlclient-dev \
		pkg-config && \
	rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=webApi.settings.settings
ENV CREDENTIALS_FILE=/app/credentials.json

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "webApi.wsgi:application"]

# Default command to run Django development server (override in docker-compose if needed)
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]