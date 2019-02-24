#!/bin/sh
#
# Part of RedELK
# Script to generate TLS certificates and SSH keys required for RedELK 
#
# Author: Outflank B.V. / Marc Smeets / @mramsmeets
#

LOGFILE="./redelk-inintialsetup.log"
INSTALLER="RedELK cert and key installer"

echoerror() {
    printf "`date +'%b %e %R'` $INSTALLER - ${RC} * ERROR ${EC}: $@\n" >> $LOGFILE 2>&1
}

echo "This script will generate necessary keys RedELK deployments"
printf "`date +'%b %e %R'` $INSTALLER - Starting installer\n" > $LOGFILE 2>&1

if ! [ $# -eq 1 ] ; then
    echo "[X] ERROR missing parameter"
    echo "[X] require 1st parameter: path of openssl config file"
    echoerror "Incorrect amount of parameters"
    exit 1
fi

if [  ! -f $1 ];then
    echo "[X]  ERROR Could not find openssl config file. Stopping"
    echoerror "Could not find openssl config file"
    exit 1
fi >> $LOGFILE 2>&1

echo "Creating dist dir if necessary"
if [ ! -d "./dist" ]; then
    mkdir ./certs
fi >> $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror " Could not create ./certs directory (Error Code: $ERROR)."
fi


echo "Creating certs dir if necessary"
if [ ! -d "./dist/certs" ]; then
    mkdir ./dist/certs
fi >> $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror " Could not create ./certs directory (Error Code: $ERROR)."
fi

echo "Generating private key for CA"
if [ ! -f "./dist/certs/redelkCA.key" ]; then 
    openssl genrsa -out ./dist/certs/redelkCA.key 2048 
fi  >> $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror "Could not generate private key for CA (Error Code: $ERROR)."
fi

echo "Copying core projects to dist directory"
cp -r ./elkserver ./dist/ >> $LOGFILE 2>&1
cp -r ./teamservers ./dist/ >> $LOGFILE 2>&1
cp -r ./redirs ./dist/ >> $LOGFILE 2>&1

echo "Creating Certificate Authority"
if [ ! -f "./dist/certs/redelkCA.crt" ]; then
    openssl req -new -x509 -days 3650 -nodes -key ./dist/certs/redelkCA.key -sha256 -out ./dist/certs/redelkCA.crt -extensions v3_ca -config $1
fi  >> $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror "Could not generate certificate authority (Error Code: $ERROR)."
fi


echo "Generating private key for ELK server"
if [ ! -f "./dist/certs/elkserver.key" ]; then
    openssl genrsa -out ./dist/certs/elkserver.key 2048
fi  >> $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror "Could not generate private key for ELK server (Error Code: $ERROR)."
fi

echo "Generating certificate for ELK server"
if [ ! -f "./dist/certs/elkserver.csr" ]; then
    openssl req -sha512 -new -key ./dist/certs/elkserver.key -out ./dist/certs/elkserver.csr -config $1
fi >> $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror "Could not generate certificates for elk server  (Error Code: $ERROR)."
fi

echo "Signing certificate of ELK server with our new CA"
if [ ! -f "./dist/certs/elkserver.crt" ]; then
    openssl x509 -days 3650 -req -sha512 -in ./dist/certs/elkserver.csr -CAcreateserial -CA ./dist/certs/redelkCA.crt -CAkey ./dist/certs/redelkCA.key -out ./dist/certs/elkserver.crt -extensions v3_req -extfile $1
fi >> $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror "Could not sign elk server certificate with CA (Error Code: $ERROR)."
fi

echo "Converting ELK server private key to PKCS8 format"
if [ ! -f "./dist/certs/elkserver.key.pem" ]; then
    cp ./dist/certs/elkserver.key ./dist/certs/elkserver.key.pem && openssl pkcs8 -in ./dist/certs/elkserver.key.pem -topk8 -nocrypt -out ./dist/certs/elkserver.key
fi  >> $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror "Could not convert ELK server private key to PKCS8 format(Error Code: $ERROR)."
fi

echo "Copying certificates to relevant redir and teamserver folders."
cp -r ./dist/certs ./dist/elkserver/logstash/ >> $LOGFILE 2>&1
cp ./dist/certs/redelkCA.crt ./dist/teamservers/filebeat/ >> $LOGFILE 2>&1
cp ./dist/certs/redelkCA.crt ./dist/redirs/filebeat/ >> $LOGFILE 2>&1

echo "Creating ssh directories if necessary"
if [ ! -d "./dist/sshkey" ] || [ ! -d "./dist/elkserver/ssh" ] || [ ! -d "./dist/teamservers/ssh" ]; then
    mkdir -p ./dist/sshkey && mkdir -p ./dist/teamservers/ssh && mkdir -p ./dist/elkserver/ssh
fi >> $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror "Could not create ssh directories (Error Code: $ERROR)."
fi

echo "Generating SSH key pair for scponly user"
if [ ! -f "./dist/sshkey/id_rsa" ] ||  [ ! -f "./dist/sshkey/id_rsa.pub" ]; then
    ssh-keygen -t rsa -f "./dist/sshkey/id_rsa" -P ""
fi >> $LOGFILE 2>&1 
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror "Could not generate SSH key pair for scponly user (Error Code: $ERROR)."
fi

echo "Copying sshkeys to relevant folders."
cp ./dist/sshkey/id_rsa.pub ./dist/elkserver/filesync/authorized_keys >> $LOGFILE 2>&1
cp ./dist/sshkey/id_rsa ./dist/teamservers/lsync/id_rsa >> $LOGFILE 2>&1

echo "Creating TGZ packages for easy distribution"
if [ ! -f "./dist/elkserver.tgz" ]; then
    tar zcvf ./dist/elkserver.tgz ./dist/elkserver/
fi >> $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror "Could not TGZ for elkserver directory (Error Code: $ERROR)."
fi
if [ ! -f "./dist/redirs.tgz" ]; then
    tar zcvf ./dist/redirs.tgz ./dist/redirs/
fi >> $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror "Could not TGZ for redirs directory (Error Code: $ERROR)."
fi
if [ ! -f "./dist/teamservers.tgz" ]; then
    tar zcvf ./dist/teamservers.tgz ./dist/teamservers/
fi >> $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror "Could not TGZ for teamserver directory (Error Code: $ERROR)."
fi

grep -i error $LOGFILE 2>$1
ERROR=$?
if [ $ERROR -eq 0 ]; then
    echo "[X] There were errors while running this installer. Manually check the log file $LOGFILE. Exiting now."
    exit
fi

echo ""
echo ""
echo "Done with initial setup."
echo "Copy the redir, teamserver or elkserver folders to every redirector, teamserver or ELK-server. Then run the relevant setup script there locally."
echo ""



