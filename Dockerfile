FROM python:3-alpine
LABEL MAINTAINER="dcueng@godaddy.com"


RUN addgroup -S dcu && adduser -H -S -G dcu dcu
RUN apk update && \ 
    apk add --no-cache build-base \
    unixodbc-dev \
    freetds-dev

COPY ./run.py ./settings.py ./logging.yaml /app/
COPY . /tmp/

RUN chown -R dcu:dcu /app

RUN PIP_CONFIG_FILE=/tmp/pip_config/pip.conf pip install --compile /tmp && rm -rf /tmp/*
WORKDIR /app

RUN echo -en "[FreeTDS]\n\
Description=FreeTDS unixODBC Driver\n\
Driver=/usr/lib/libtdsodbc.so\n" > /etc/odbcinst.ini

ENTRYPOINT ["python", "/app/run.py"]