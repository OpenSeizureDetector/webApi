#! /bin/bash
# From https://github.com/leafney/ubuntu-mysql/blob/master/startup.sh
set -e

######################################################
# Specify the database access credentials here
DATA_DIR=/opt/osdData
MYSQL_ROOT_PWD=${MYSQL_ROOT_PWD:-"mysql"}
OSD_USER=${OSD_USER:-"osd"}
OSD_USER_PWD=${OSD_USER_PWD:-"replace-me-with-secret-password"}
OSD_USER_DB=${OSD_USER_DB:-"osd"}
FIRST_RUN_FILE=${DATA_DIR}/firstrun
SECRET_KEY="replace-me-with-secret-key"
OSD_EMAIL_HOSTNAME="osdapi.ddns.net"
OSD_EMAIL_UNAME="osd_api"

if [ ! -e $FIRST_RUN_FILE ]; then
    #############################
    # Set up persistent storage #
    #############################
    echo "Setting up persistant data directory"
    df
    mkdir -p $DATA_DIR
    mkdir -p ${DATA_DIR}/lib
    mkdir -p ${DATA_DIR}/log/mysql 
    echo "Creating first run file "$FIRST_RUN_FILE
    touch $FIRST_RUN_FILE
    ls -la $FIRST_RUN_FILE
    ls -la /var/lib/mysql
    cp -rf /var/lib/mysql ${DATA_DIR}/lib 
    rm -rf /var/lib/mysql 
    ln -sf ${DATA_DIR}/lib/mysql /var/lib/mysql 
    ln -sf ${DATA_DIR}/log/mysql /var/log/mysql 
    mkdir -p /var/run/mysqld  
    chown -R mysql.mysql ${DATA_DIR}/lib/mysql  
    chown -R mysql.mysql /var/run/mysqld  
    chown -R mysql.mysql ${DATA_DIR}/log/mysql 
    ls -la /var/lib/mysql/
    ls -la ${DATA_DIR}/lib/mysql

    ####################################################
    # Setup MySQL
    ####################################################
    echo "Starting MySQL"
    service mysql start

    echo "[i] Setting root new password."
    mysql --user=root --password=root -e "SET PASSWORD FOR 'root'@'localhost' = '$MYSQL_ROOT_PWD'; FLUSH PRIVILEGES;"

    echo "[i] Granting root privileges."
    mysql --user=root --password=$MYSQL_ROOT_PWD -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost'; FLUSH PRIVILEGES;"

    if [ -n "$OSD_USER_DB" ]; then
	echo "[i] Creating datebase: $OSD_USER_DB"
	mysql --user=root --password=$MYSQL_ROOT_PWD -e "CREATE DATABASE IF NOT EXISTS \`$OSD_USER_DB\` CHARACTER SET utf8 COLLATE utf8_general_ci; FLUSH PRIVILEGES;"
	
	if [ -n "$OSD_USER" ] && [ -n "$OSD_USER_PWD" ]; then
	    echo "[i] Create new User: $OSD_USER with password $OSD_USER_PWD for new database $OSD_USER_DB."
	    mysql --user=root --password=$MYSQL_ROOT_PWD -e "CREATE USER '$OSD_USER'@'localhost' IDENTIFIED BY '$OSD_USER_PWD'; GRANT ALL PRIVILEGES ON \`$OSD_USER_DB\`.* TO '$OSD_USER'@'localhost'; FLUSH PRIVILEGES;"
	else
	    echo "[i] Don\`t need to create new User."
	fi
    else
	echo "No User Database Specified - doing nothing..."
    fi
    cd ${DATA_DIR}
    git clone https://github.com/OpenSeizureDetector/webApi.git
    cp webApi/api/webApi/credentials.json.template webApi/api/webApi/credentials.json 
    sed -i 's/"db_name" : "",/"db_name" : "'$OSD_USER_DB'",/g' webApi/api/webApi/credentials.json 
    sed -i 's/"db_user" : "",/"db_user" : "'$OSD_USER'",/g' webApi/api/webApi/credentials.json 
    sed -i 's/"db_password" : "",/"db_password" : "'$OSD_USER_PWD'",/g' webApi/api/webApi/credentials.json 
    sed -i 's/"secret_key" : "",/"secret_key" : "'$SECRET_KEY'",/g' webApi/api/webApi/credentials.json 
    sed -i 's/"email_host" : "",/"email_host" : "'$OSD_EMAIL_HOSTNAME'",/g' webApi/api/webApi/credentials.json 
    sed -i 's/"email_host_user" : "",/"email_host_user" : "'$OSD_EMAIL_UNAME'",/g' webApi/api/webApi/credentials.json 
    cat webApi/api/webApi/credentials.json 
    python3 webApi/api/manage.py makemigrations 
    python3 webApi/api/manage.py migrate 
    
    ####################################################
    # Setup nginx
    ####################################################
    cp webApi/etc/nginx/sites-available/webApi /etc/nginx/sites-available 
    ln -s /etc/nginx/sites-available/webApi /etc/nginx/sites-enabled/webApi 
    echo "Testing nginx configuration...." 
    nginx -t 
    systemctl enable nginx



    #killall mysqld
    #sleep 5
    echo "[i] Setting end,have fun."
    rm $FIRST_RUN_FILE
else
    echo "$FIRST_RUN_FILE exists - not initialising system"
fi

# Start Services
ln -s ${DATA_DIR}/lib/mysql /var/lib/mysql 
ln -s ${DATA_DIR}/log/mysql /var/log/mysql 
service mysql start

service nginx start
    

# Run the command from the command line?
exec "$@"
