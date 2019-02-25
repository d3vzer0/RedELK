FROM python:3.6-alpine

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

ARG VERBOSITY=0
ENV VERBOSITY="${VERBOSITY}"

ARG INTERVAL=3600
ENV INTERVAL="${INTERVAL}"

# Infra variables
ARG KAFKA_HOST=kafka:29092
ENV KAFKA_HOST="${KAFKA_HOST}"

ARG ELASTIC_HOST=elasticsearch:9200
ENV ELASTIC_HOST="${ELASTIC_HOST}"

ARG REDIS_IP=redis_service
ENV REDIS_IP="${REDIS_IP}"

ARG REDIS_PORT=6379
ENV REDIS_PORT="${REDIS_PORT}"

# Virustotal API Config
ARG VTURL="https://www.virustotal.com/vtapi/v2/file/report"
ENV VTURL="${VTURL}"

ARG VTKEY=""
ENV VTKEY="${VTKEY}"

# XForce API Config
ARG XFORCEURL="https://api.xforce.ibmcloud.com"
ENV XFORCEURL="${XFORCEURL}"

ARG XFORCEPASS=""
ENV XFORCEPASS="${XFORCEPASS}"

ARG XFORCEKEY=""
ENV XFORCEKEY="${XFORCEKEY}"

# HybridAnalyis API Config
ARG HAURL="https://www.hybrid-analysis.com/api/v2/search"
ENV HAURL="${HAURL}"

ARG HAKEY=""
ENV HAKEY="${HAKEY}"

# Greynoise API Config
ARG GREYURL="http://api.greynoise.io:8888/v1/query/ip"
ENV GREYURL="${GREYURL}"

# Cache settings for Intel
ARG CACHE_VT=3600
ENV CACHE_VT="${CACHE_VT}"

ARG CACHE_GREY=3600
ENV CACHE_GREY="${CACHE_GREY}"

ARG CACHE_XFORCE=3600
ENV CACHE_XFORCE="${CACHE_XFORCE}"

ARG CACHE_HA=3600
ENV CACHE_HA="${CACHE_HA}"

WORKDIR /intel
COPY . .


