# Dockerfile following the Udemy course https://www.udemy.com/course/django-python-advanced 
# most probably this is Dockerfile is highly unsafe
# see https://pythonspeed.com/articles/dockerizing-python-is-hard/ 
# and https://pythonspeed.com/articles/base-image-python-docker-images/ for improvements
FROM python:3.8-alpine3.11
# use LABEL instead of deprecated MAINTAINER 
LABEL maintainer="thomas-schild unmaintained"

# do not buffer any output but write it directly output
ENV PYTHONUNBUFFERED 1 

# install the postgres client via apk 
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps  gcc libc-dev linux-headers postgresql-dev
# install dependencies
# probably it would be a better idea to list dependencies explicitly within the Dockfile
# the receipe app depends on https://www.djangoproject.com/, https://www.django-rest-framework.org 
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
# cleanup temp deps
RUN apk del .tmp-build-deps

# setup workdir and copy
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# create a USER to run the image (avoid running as root)
RUN adduser -D receipe-user
USER receipe-user
