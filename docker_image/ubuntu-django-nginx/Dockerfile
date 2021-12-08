################################################################
# OpenSeizureDetector webAPI Docker Image Creator (Dockerfile) #
################################################################
FROM ubuntu:20.04

ARG APT_OPTIONS="-y -q"
ARG DEBIAN_FRONTEND="noninteractive"

SHELL ["/bin/bash", "-c"]

RUN set -xe \
&& apt-get update \
&& apt-get $APT_OPTIONS install python3 python3-pip python3-dev python3-venv \
                                git libmysqlclient-dev vim mysql-server  \
				npm supervisor nginx snapd mailutils \
&& echo "Finished APT installations" \
#&& service snapd start \
#&& service mysql start \
&& pip3 -q install mysqlclient \
                  django-rest-registration django-filter django-cors-headers \
		  numpy \
		  gunicorn \
&& echo "Finished PIP installations" \
#&& snap install core \
#&& snap refresh core \
#&& snap install --classic certbot \
#&& ln -s /snap/bin/certbot /usr/bin/certbot \
#&& echo "Finished snap installations" \

