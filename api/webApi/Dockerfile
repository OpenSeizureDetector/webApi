FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=webApi.settings
ENV CREDENTIALS_FILE=/app/credentials.json

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "webApi.wsgi:application"]