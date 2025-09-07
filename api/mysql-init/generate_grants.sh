#!/bin/bash
# Auto-generate init_grants.sql from environment variables


# Use environment variables directly
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQL_FILE="$SCRIPT_DIR/init_grants.sql"
USER="${MYSQL_USER}"
DB="${MYSQL_DATABASE}"
PASS="${MYSQL_PASSWORD}"

if [ -z "$USER" ] || [ -z "$DB" ] || [ -z "$PASS" ]; then
  echo "ERROR: One or more required environment variables (MYSQL_USER, MYSQL_DATABASE, MYSQL_PASSWORD) are not set."
  exit 1
fi


cat > "$SQL_FILE" <<EOF
CREATE USER IF NOT EXISTS '${USER}'@'%' IDENTIFIED BY '${PASS}';
GRANT ALL ON ${DB}.* TO '${USER}'@'%';
FLUSH PRIVILEGES;
EOF

echo "Generated $SQL_FILE with user: $USER, database: $DB"
