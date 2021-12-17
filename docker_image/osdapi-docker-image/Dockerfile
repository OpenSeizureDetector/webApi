################################################################
# OpenSeizureDetector webAPI Docker Image Creator (Dockerfile) #
################################################################
FROM ubuntu-django-nginx:latest



######################################################
# Do not alter anything below here!!!!
#
ARG DATA_DIR=/opt/osdData

SHELL ["/bin/bash", "-c"]

RUN set -xe \
&& usermod -d/var/lib/mysql mysql 

EXPOSE 3306
EXPOSE 80
COPY ./startup.sh /root/startup.sh
RUN chmod +x /root//startup.sh
ENTRYPOINT ["/root/startup.sh"]