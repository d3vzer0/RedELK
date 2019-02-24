FROM alpine:latest

# Install lsync and openssh-client
RUN apk update && apk add lsyncd openssh-client openssl

# Create base user that syncs files to ELK server
RUN adduser --home /home/scponly --gecos "" --disabled-password scponly
