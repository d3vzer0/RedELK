#!/bin/sh
#
# Part of RedELK
# Script to install RedELK on Cobalt Strike teamservers
#
# Author: Outflank B.V. / Marc Smeets 
#

LOGFILE="redelk-install.log"
INSTALLER="RedELK teamserver installer"

echoerror() {
    printf "`date +'%b %e %R'` $INSTALLER - ${RC} * ERROR ${EC}: $@\n" >> $LOGFILE 2>&1
}

echo "This script will install and configure necessary components for RedELK on Cobalt Strike teamservers"
printf "`date +'%b %e %R'` $INSTALLER - Starting installer\n" > $LOGFILE 2>&1

if ! [ $# -eq 3 ] ; then
    echo "[X] ERROR Incorrect amount of parameters"
    echo "[X] require 1st parameter: identifier of this machine to set in filebeat config."
    echo "[X] require 2nd parameter: attackscenario name."
    echo "[X] require 3rd parameter: IP/DNS:port where to ship logs to."
    echoerror "Incorrect amount of parameters"
    exit 1
fi

echo "Altering hostname field in filebeat config"
sed -i s/'@@HOSTNAME@@'/$1/g ./etc/filebeat/filebeat.yml  >> $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror "Could not change hostname field in filebeat config (Error Code: $ERROR)."
fi

echo "Altering attackscenario field in filebeat config "
sed -i s/'@@ATTACKSCENARIO@@'/$2/g ./etc/filebeat/filebeat.yml >> $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror "Could not change attackscenario field in filebeat config (Error Code: $ERROR)."
fi

echo "Altering log destination field in filebeat config "
sed -i s/'@@HOSTANDPORT@@'/$3/g ./etc/filebeat/filebeat.yml >> $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror "Could not change log destination field in filebeat config (Error Code: $ERROR)."
fi

grep -i error $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -eq 0 ]; then
    echo "[X] There were errors while running this installer. Manually check the log file $LOGFILE. Exiting now."
    exit
fi

echo ""
echo ""
echo "Done with setup of RedELK on teamserver."
echo ""
