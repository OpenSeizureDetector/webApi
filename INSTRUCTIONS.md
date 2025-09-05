# OpenSeizureDetector/webApi - Docker & MySQL Setup

## Prerequisites
- Docker & Docker Compose installed

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/OpenSeizureDetector/webApi.git
   cd webApi
   ```

2. **Prepare Credentials**
   - Copy the template and edit as needed:
     ```bash
     cp api/webApi/credentials.json.template api/webApi/credentials.json
     ```
   - Edit `api/webApi/credentials.json` to match your MySQL values.

3. **Build and Run Containers**
   ```bash
   docker-compose up --build
   ```

   - The first run initializes MySQL and starts the Django API.

4. **Initialize Django Database**
   - Open a shell in the webApi container:
     ```bash
     docker-compose exec webapi bash
     ```
   - Run migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

5. **Access the API**
   - Visit [http://localhost:8000](http://localhost:8000)

6. **Stopping**
   ```bash
   docker-compose down
   ```

## Notes
- Django will create all tables on first migration.
- Use `init_db.sql` to pre-seed categories if required.
- To create an admin user:
   ```bash
   docker-compose exec webapi python manage.py createsuperuser
   ```

## Security
- The credentials file should **not** be tracked in git!
- For production, mount a different credentials file using a Docker volume or set `CREDENTIALS_FILE` env var.
