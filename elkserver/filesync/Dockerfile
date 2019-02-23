FROM alpine:latest

# Install openssh daemon and RSSH (scp only shell)
RUN apk update && apk add openssl openssh rssh

# Create SCP only user without ability to login via password
RUN adduser --home /home/scponly --disabled-password scponly
    
# Add scponly user to rssh config
COPY ./config/rssh.conf /etc/rssh.conf

# Generate host keys
RUN ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa
RUN ssh-keygen -f /etc/ssh/ssh_host_dsa_key -N '' -t dsa
RUN ssh-keygen -f /etc/ssh/ssh_host_ed25519_key -N '' -t ed25519
RUN ssh-keygen -f /etc/ssh/ssh_host_ecdsa_key -N '' -t ecdsa 

# Run SSH daemon
CMD ["/usr/sbin/sshd","-D"]
