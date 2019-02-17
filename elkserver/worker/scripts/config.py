import os

# Verbosity
Verbosity = os.getenv['VERBOSITY'] 

# interval for rechecking IOC's
interval = os.getenv['INTERVAL']

#### API
api_keys = {
    'virustotal': {
        'url':  os.getenv['VTURL'],
        'key':  os.getenv['VTKEY'] 
    },
    'greynoise': {
        'url':  os.getenv['GREYURL'] ,
    },
    'xforce': {
        'url': os.getenv['XFORCEURL'] ,
        'key': os.getenv['XFORCEKEY'] ,
        'password': os.getenv['XFORCEPASS'] 
    },
    'hybridanalysis': {
        'url': os.getenv['HAURL'] ,
        'key': os.getenv['HAKEY'] 
    }
}

#### SMTP settings
smtpSrv= os.getenv['SMTPIP']
smtpPort= os.getenv['SMTPORT']
smtpName= os.getenv['SMTPNAME']
smtpPass= os.getenv['SMTPPASS']
fromAddr= os.getenv['FROMADDR']
toAddr= os.getenv['TOADDR']

#### directory for cache files (including shelves)
tempDir= os.getenv['TEMPDIR']
