FROM python:3.6

RUN apt-get update && apt-get -y upgrade && apt-get -y install gcc python3-dev cron busybox 

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

ARG VERBOSITY=0
ENV VERBOSITY="${VERBOSITY}"

ARG INTERVAL=3600
ENV INTERVAL="${INTERVAL}"

ARG ELASTIC_IP=http://elasticsearch
ENV ELASTIC_IP="${ELASTIC_IP}"

ARG ELASTIC_PORT=9200
ENV ELASTIC_PORT="${ELASTIC_PORT}"

ARG VTKEY=""
ENV VTKEY="${VTKEY}"

ARG XFORCEAUTH="Basic: "
ENV XFORCEAUTH="${XFORCEAUTH}"

ARG HAKEY=""
ENV HAKEY="${HAKEY}"

ARG SMTPIP="mailserver.nl"
ENV SMTPIP="${SMTPIP}"

ARG SMTPORT=587
ENV SMTPORT="${SMTPORT}"

ARG SMTPNAME="root"
ENV SMTPNAME="${SMTPNAME}"

ARG SMTPPASS="toor"
ENV SMTPPASS="${SMTPPASS}"

ARG FROMADDR="your@address.here"
ENV FROMADDR="${FROMADDR}"

ARG TOADDR="your@address.here"
ENV TOADDR="${TOADDR}"

ARG TEMPDIR="/tmp"
ENV TEMPDIR="${TEMPDIR}"

# Create redelk config dir
RUN mkdir -p /etc/redelk

# Create scripts dir and set permissions
RUN mkdir -p /usr/share/redelk/bin
COPY ./scripts/* /usr/share/redelk/bin/
RUN chmod -R 775 /usr/share/redelk/bin/*

# Copy cron tasks
COPY ./cron.d/redelk /etc/cron.d/redelk

CMD python run.py


