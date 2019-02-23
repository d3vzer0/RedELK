
LOGFILE="redelk-install.log"
INSTALLER="RedELK elkserver installer"
CWD=`pwd`

echoerror() {
    printf "`date +'%b %e %R'` $INSTALLER - ${RC} * ERROR ${EC}: $@\n" >> $LOGFILE 2>&1
}

echo "This script will install and configure necessary components for RedELK on ELK server"
printf "`date +'%b %e %R'` $INSTALLER - Starting installer\n" > $LOGFILE 2>&1


echo "Installing Kibana template"
curl -X POST "http://localhost:5601/api/saved_objects/_bulk_create" -H 'kbn-xsrf: true' -H "Content-Type: application/json" -d @./templates/redelk_kibana_all.json >> $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror "Could not install Kibana template (Error Code: $ERROR)."
fi

# setting default index to d76c6b70-b617-11e8-bc1a-cf8fa3255855 == rtops-*
echo "Setting the Kibana default index"
curl -X POST "http://localhost:5601/api/kibana/settings/defaultIndex" -H "Content-Type: application/json" -H "kbn-xsrf: true" -d"{\"value\":\"d76c6b70-b617-11e8-bc1a-cf8fa3255855\"}" >> $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror "Could not set the default index for Kibana (Error Code: $ERROR)."
fi


echo "Installing GeoIP index template adjustment"
curl -XPUT -H 'Content-Type: application/json' http://localhost:9200/_template/redirhaproxy- -d@./templates/elasticsearch-template-geoip-es6x.json >> $LOGFILE 2>&1
ERROR=$?
if [ $ERROR -ne 0 ]; then
    echoerror "Could not install GeoIP index template adjust (Error Code: $ERROR)."
fi

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

