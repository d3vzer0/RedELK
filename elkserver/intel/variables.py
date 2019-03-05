import os

api_keys = {
    'virustotal': {
        'url':  os.getenv('VTURL', 'https://www.virustotal.com/vtapi/v2/file/report'),
        'key':  os.getenv('VTKEY', None),
        'topic': 'intel-virustotal'
    },
    'greynoise': {
        'url':  os.getenv('GREYURL', 'http://api.greynoise.io:8888/v1/query/ip'),
        'topic': 'intel-greynoise'
    },
    'xforce': {
        'url': os.getenv('XFORCEURL', 'https://api.xforce.ibmcloud.com'),
        'key': os.getenv('XFORCEKEY', None),
        'password': os.getenv('XFORCEPASS', None) ,
        'topic': 'intel-xforce'
    },
    'hybridanalysis': {
        'url': os.getenv('HAURL', 'https://www.hybrid-analysis.com/api/v2/search'),
        'key': os.getenv('HAKEY', None),
        'topic': 'intel-hybridanalysis'
    }
}

config = {
    'kafka': {
        'host': os.getenv('KAFKA_HOST', 'localhost:9092'),
    },
    'elasticsearch': {
        'host': os.getenv('ELASTIC_HOST', 'localhost:9200'),
    },
    'redis': {
        'ip': os.getenv('REDIS_IP', 'localhost'),
        'port': int(os.getenv('REDIS_PORT', 6379))
    },
    'cache': {
        'virustotal': int(os.getenv('CACHE_VT', 3600)),
        'greynoise': int(os.getenv('CACHE_GREY', 3600)),
        'xforce': int(os.getenv('CACHE_XFORCE', 3600)),
        'hybridanalysis': int(os.getenv('CACHE_HA', 3600))
    }
}
