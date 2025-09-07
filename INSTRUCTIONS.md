# OpenSeizureDetector/webApi - Docker & MySQL Setup

## Prerequisites
- Docker & Docker Compose installed

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/OpenSeizureDetector/webApi.git
   cd webApi
   ```

2. **Create your `.env` file**
   - Copy the template and edit as needed:
     ```bash
     cp api/.env.template api/.env
     ```
   - Edit `api/.env` to set your MySQL and Django environment variables.

3. **Generate MySQL grants file**
   - Run the grant script (on host or in container with correct permissions):
     ```bash
     cd api/mysql-init
     bash generate_grants.sh
     ```
   - If you run the script inside the container, fix permissions:
     ```bash
     sudo chown -R 999:999 api/mysql-init
     # or
     sudo chmod -R 777 api/mysql-init
     ```

4. **Build and Run Containers**
   ```bash
   docker-compose up --build
   ```
   - The first run initializes MySQL and starts the Django API.

5. **Initialize Django Database**
   - Open a shell in the webApi container:
     ```bash
     docker-compose exec webapi bash
     ```
   - Run migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

6. **Access the API**

   - Visit [http://localhost:8000](http://localhost:8000)

## Migrating a MySQL Database to a New Server

To dump an existing MySQL database and import it into a new one on a different server:

### 1. Dump the database on the source server
```bash
mysqldump -u <user> -p<password> <database_name> > db_dump.sql
```

### 2. Copy the dump file to the new server
```bash
scp db_dump.sql <user>@<new_server_ip>:/path/to/db_dump.sql
```

### 3. Import the dump into the new MySQL server
On the new server:
```bash
mysql -u <user> -p<password> <database_name> < /path/to/db_dump.sql
```

Replace `<user>`, `<password>`, and `<database_name>` with your actual MySQL credentials and database name.

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
