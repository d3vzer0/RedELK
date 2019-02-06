import os

#### General
# Verbosity
Verbosity = os.getenv['VERBOSITY'] 

# interval for rechecking IOC's
interval = os.getenv['INTERVAL'] 

#### Virustotal API
vt_apikey = os.getenv['VTKEY']

#### IBM X-Force API (can be retreived from a sample call on their swagger test site)
ibm_BasicAuth = os.getenv['XFORCEAUTH']

#### HybridAnalysisAPIKEY
HybridAnalysisAPIKEY = os.getenv['HAKEY']

#### SMTP settings
smtpSrv= os.getenv['SMTPIP']
smtpPort= os.getenv['SMTPORT']
smtpName= os.getenv['SMTPNAME']
smtpPass= os.getenv['SMTPPASS']
fromAddr= os.getenv['FROMADDR']
toAddr= os.getenv['TOADDR']

#### directory for cache files (including shelves)
tempDir= os.getenv['TEMPDIR']
