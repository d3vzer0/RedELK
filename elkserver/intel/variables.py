import os

api_keys = {
    'virustotal': {
        'url':  os.environ['VTURL'],
        'key':  os.environ['VTKEY'] 
    },
    'greynoise': {
        'url':  os.environ['GREYURL'] ,
    },
    'xforce': {
        'url': os.environ['XFORCEURL'] ,
        'key': os.environ['XFORCEKEY'] ,
        'password': os.environ['XFORCEPASS'] 
    },
    'hybridanalysis': {
        'url': os.environ['HAURL'] ,
        'key': os.environ['HAKEY'] 
    }
}

config = {
    'kafka': {
        'host': os.environ['KAFKA_HOST'],
        'produce_topic': os.environ['PRODUCER_TOPIC'],
    },
    'elasticsearch': {
        'host': os.environ['ELASTIC_HOST'],
    },
    'redis': {
        'ip': os.environ['REDIS_IP'],
        'port': int(os.environ['REDIS_PORT'])
    },
    'cache': {
        'virustotal': int(os.environ['CACHE_VT']),
        'greynoise': int(os.environ['CACHE_GREY']),
        'xforce': int(os.environ['CACHE_XFORCE']),
        'hybridanalysis': int(os.environ['CACHE_HA'])
    }
}
