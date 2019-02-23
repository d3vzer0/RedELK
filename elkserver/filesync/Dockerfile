FROM alpine:latest

# Install openssh daemon and RSSH (scp only shell)
RUN apk update && apk add openssl openssh rssh

# Create SCP only user without ability to login via password
RUN adduser --home /home/scponly --disabled-password scponly
    
# Add scponly user to rssh config
COPY ./config/rssh.conf /etc/rssh.conf

# Run SSH daemon
CMD ["/usr/sbin/sshd","-D"]
