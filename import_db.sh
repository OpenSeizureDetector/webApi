#!/bin/bash

# Usage: ./import_db.sh <mysql_container_name> <db_user> <db_password> <db_name> <backup_file>
# Example: ./import_db.sh mysql osd osdpwd osd /path/to/osd_backup.sql

MYSQL_CONTAINER="$1"
DB_USER="$2"
DB_PASSWORD="$3"
DB_NAME="$4"
BACKUP_FILE="$5"

if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <mysql_container_name> <db_user> <db_password> <db_name> <backup_file>"
    exit 1
fi

echo "Copying backup file into container..."
docker cp "$BACKUP_FILE" "$MYSQL_CONTAINER":/osd_backup.sql

echo "Importing database..."
docker exec -i "$MYSQL_CONTAINER" mysql -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < /osd_backup.sql

echo "Setting AUTO_INCREMENT for datapoints and events tables..."
MAX_DP=$(docker exec -i "$MYSQL_CONTAINER" mysql -u "$DB_USER" -p"$DB_PASSWORD" -N -e "SELECT MAX(id) FROM $DB_NAME.datapoints;")
MAX_EV=$(docker exec -i "$MYSQL_CONTAINER" mysql -u "$DB_USER" -p"$DB_PASSWORD" -N -e "SELECT MAX(id) FROM $DB_NAME.events;")

docker exec -i "$MYSQL_CONTAINER" mysql -u "$DB_USER" -p"$DB_PASSWORD" -e "ALTER TABLE $DB_NAME.datapoints AUTO_INCREMENT = $((MAX_DP+1));"
docker exec -i "$MYSQL_CONTAINER" mysql -u "$DB_USER" -p"$DB_PASSWORD" -e "ALTER TABLE $DB_NAME.events AUTO_INCREMENT = $((MAX_EV+1));"

echo "Database import and primary key initialization complete."
