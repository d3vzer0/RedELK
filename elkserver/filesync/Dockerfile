FROM alpine:latest

# Install openssh daemon and RSSH (scp only shell)
RUN apk update && apk add openssl openssh rssh shadow

# Create SCP only user without ability to login via password (pubkey only)
RUN adduser --home /home/scponly --gecos "" --disabled-password scponly
RUN usermod -p '*' scponly

# Add scponly user to rssh config
COPY ./config/rssh.conf /etc/rssh.conf
COPY ./config/sshd_config /etc/ssh/sshd_config

# Generate host keys
RUN ssh-keygen -A

# Run SSH daemon
CMD ["/usr/sbin/sshd","-D"]
