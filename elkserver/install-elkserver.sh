#!/bin/sh
#
# Part of RedELK
# Script to install RedELK on ELK server
#
# Author: Outflank B.V. / Marc Smeets 
#


LOGFILE="redelk-install.log"
INSTALLER="RedELK elkserver installer"
CWD=`pwd`

echoerror() {
    printf "`date +'%b %e %R'` $INSTALLER - ${RC} * ERROR ${EC}: $@\n" >> $LOGFILE 2>&1
}

echo "This script will install and configure necessary components for RedELK on ELK server"
printf "`date +'%b %e %R'` $INSTALLER - Starting installer\n" > $LOGFILE 2>&1


echo "Downloading GeoIP database files"
cd ./elkserver/logstash/geoip && curl http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz -O >> $LOGFILE 2>&1 && curl http://geolite.maxmind.com/download/geoip/database/GeoLite2-ASN.tar.gz -O >> $LOGFILE 2>&1 && tar zxvf /tmp/GeoLite2-ASN.tar.gz >> $LOGFILE 2>&1 && tar zxvf /tmp/GeoLite2-City.tar.gz
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror "Could not download geoIP database files (Error Code: $ERROR)."
fi
cd $CWD


# Change behaviour to overwrite docker-based kibana logo
# echo "Inserting the superawesomesauce RedELK logo into Kibana"
# cp /usr/share/kibana/optimize/bundles/commons.style.css /usr/share/kibana/optimize/bundles/commons.style.css.ori && cp ./kibana/* /usr/share/kibana/optimize/bundles/ >> $LOGFILE 2>&1
# ERROR=$?
# if [ $ERROR -ne 0 ]; then
#     echoerror "Could not adjust Kibana logo (Error Code: $ERROR)."
# fi

grep -i error $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -eq 0 ]; then
    echo "[X] There were errors while running this installer. Manually check the log file $LOGFILE. Exiting now."
    exit
fi

echo ""
echo ""
echo "Done with base setup of RedELK on ELK server"
echo ""
echo "WARNING - YOU STILL NEED TO ADJUST CONFIG FILES"
echo " - adjust the /etc/cron.d/redelk file to include your teamservers"
echo " - adjust all config files in /etc/redelk/"
echo ""
echo "You can now login to RedELK Kibana on this machine using redelk:redelk as credentials."
echo ""

