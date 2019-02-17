FROM alpine:3.9

# Note:
# Make sure that the host has the TPROX Kernel module enabled
# modprobe xt_TPROXY && echo xt_TPROXY >> /etc/modules

# Install generic buildtools
RUN apk add build-base linux-headers

# Download and extract latest version of HAProxy
RUN wget -O /tmp/haproxy-1.8.19.tar.gz http://www.haproxy.org/download/1.8/src/haproxy-1.8.19.tar.gz
RUN tar -xzf /tmp/haproxy-1.8.19.tar.gz -C /tmp/

# Change working directory and build Haproxy with TPROX support
WORKDIR /tmp/haproxy-1.8.19
RUN make TARGET=linux26 USE_LINUX_TPROXY=1
RUN make install target=linux26
RUN cp /usr/local/sbin/haproxy /usr/sbin/haproxy
RUN mkdir /etc/haproxy

# Change working directory and start haproxy in debug mode
WORKDIR /etc/haproxy
CMD ["haproxy", "-d", "-f", "haproxy.cfg"]