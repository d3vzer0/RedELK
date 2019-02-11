FROM python:3.6-alpine

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Infra variables
ARG KAFKA_HOST=kafka:9092
ENV KAFKA_HOST="${KAFKA_HOST}"

ARG ELASTIC_HOST=elasticsearch:9200
ENV ELASTIC_HOST="${ELASTIC_HOST}"

# Kafka Settings
ARG CONSUMER_GROUP=consumer-newbeacons-enricher
ENV CONSUMER_GROUP="${CONSUMER_GROUP}"

ARG CONSUMER_TOPIC=cs-beacons
ENV CONSUMER_TOPIC="${CONSUMER_TOPIC}"

ARG PRODUCER_TOPIC=cs-beacons-enriched
ENV PRODUCER_TOPIC="${PRODUCER_TOPIC}"

# Create redelk config dir
WORKDIR /enrich
COPY . .

CMD python enricher.py


