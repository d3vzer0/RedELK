FROM openjdk:11-stretch

# Set defaults for teamserver
ARG TS_IP=127.0.0.1
ENV TS_IP="${TS_IP}"

ARG TS_PASSWORD=you_should_change_this
ENV TS_PASSWORD="${TS_PASSWORD}"

# Run teamserver with default variables
CMD /opt/cobaltstrike/teamserver ${TS_IP} ${TS_PASSWORD}