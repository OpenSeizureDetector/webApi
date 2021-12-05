FROM ubuntu:18.04

ARG APT_OPTIONS="-y -q"
ARG VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
ARG WORKON_HOME=$HOME/.virtualenvs
ARG VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
ARG DEBIAN_FRONTEND="noninteractive"

SHELL ["/bin/bash", "-c"]

RUN set -xe \
&& apt-get update \
&& apt-get $APT_OPTIONS install python3 python3-pip python3-dev python3-venv \
&& apt-get $APT_OPTIONS install git libmysqlclient-dev vim \
&& apt-get $APT_OPTIONS install mysql-server || echo "OK" \
&& mkdir /var/run/mysqld \
&& chown mysql /var/run/mysqld \
&& /etc/init.d/mysql start \
&& mysql -uroot --password="" -e "CREATE USER 'garmin'@'localhost' IDENTIFIED BY '';" || echo "OK" \
&& mysql -uroot --password="" -e "GRANT ALL PRIVILEGES ON *.* TO 'garmin'@'localhost';" || echo "OK" \
&& mysql -u garmin --password="" -e "CREATE DATABASE garmin_OSDDB"  || echo "OK" \
&& pip3 -q install mysqlclient django-rest-registration django-filter numpy django-cors-headers \
&& git clone https://github.com/OpenSeizureDetector/webApi.git \
&& cp webApi/api/webApi/credentials.json.template webApi/api/webApi/credentials.json \
&& sed -i 's/"db_name" : "",/"db_name" : "garmin_OSDDB",/g' webApi/api/webApi/credentials.json \
&& sed -i 's/"db_user" : "",/"db_user" : "garmin",/g' webApi/api/webApi/credentials.json \
&& python3 webApi/api/manage.py makemigrations \
&& python3 webApi/api/manage.py migrate
