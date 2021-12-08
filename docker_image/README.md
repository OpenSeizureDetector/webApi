Docker_Image README
===================

This folder contains the files necessary to build a docker image of the
osdApi server to help installation on remove machines.

Building the image is a two stage proecss - it is two stage so that
the slow activities (installing all the software from repositories)
can be run infrequenty during development.
The second stage (configuring for osdApi is then quick to run, as we are
having to do this a lot during development!

Stage 1
=======
Build the ubuntu-django-nginx docker image:

```
cd ubuntu-django-nginx
time docker build -t ubuntu-django-nginx .
```
Takes about 6 minutes on my laptop.

Stage 2
=======
build osdapi-docker-image (which is based on ubuntu-django-nginx).
```
cd ../osdapi-docker-image
time docker build -t osdapi-docker-image
```

Run the image
=============
Create a folder on the host machine to store configuration files and the database:
```
mkdir /opt/osdData
```

Run the image, giving a shell prompt to check what it is doing.
The first start up downloads the webApi code into the image and creates the necessary files.
It uses
```
docker run -it osdapi-docker-image --mount type=bind,source=/opt/osdData/,target=opt/osdData bash
```

TODO:
  * Sort out how to deal with letsencrypt
  * Pass the relevant ports from the container to the host so the container is visible on the network.