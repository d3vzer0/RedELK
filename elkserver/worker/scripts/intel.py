from elasticsearch import Elasticsearch
from kafka import KafkaProducer
from config_local import api_keys
import hashlib
import redis
import json
import requests
import csv


class ContextFile:
    def __init__(self, path='./lookups'):
        self.path = path
    
    def get_indicators(self, lookup='indicators_md5.csv'):
        file_path = '{}/{}'.format(self.path, lookup)
        csv_object = csv.DictReader(open(file_path), delimiter=';')
        primary_field = csv_object.fieldnames[0]
        result = [row[primary_field] for row in csv_object]
        return result


class ContextES:
    def __init__(self):
        self.es = Elasticsearch(['localhost:9200'])
        self.beacon_index = "beacondb*"
        self.rtops_index = "rtops*"

    def get_unique_extips(self, result=[]):
        dsl_query = {'size':0, 'aggregations':{
            'unique_ips': {'terms':{'field':'target_ipext.keyword'}}}}
        query_ips = self.es.search(index=self.rtops_index, body=dsl_query)
        for ip in query_ips['aggregations']['unique_ips']['buckets']:
            result.append(ip['key'])
        return result

    def get_beacons(self):
        beacons = self.es.search(index=self.beacon_index)['hits']['hits']
        return beacons


class Intel:
    def __init__(self, server='localhost', **kwargs):
        self.kwargs = kwargs
        self.rserver = redis.Redis(host=server, port=6379, db=0)
        self.cache = {
            'virustotal': 3600,
            'greynoise': 3600,
            'xforce': 3600
        }

    def check_cache(self, job, value):
        job_name = '{}-{}'.format(job, value)
        job_id = hashlib.md5(job_name.encode('utf-8')).hexdigest()
        get_cache = self.rserver.get(job_id)
        records = json.loads(get_cache) if get_cache is not None else []
        return {'job_id':job_id, 'records':records}

    def greynoise(self):
        result = self.check_cache('greynoise', self.kwargs['ip'])
        if not result['records']:
            greynoise = requests.post(api_keys['greynoise']['url'], data={'ip':self.kwargs['ip']}).json()
            result['records'] = greynoise.get('records', [])
            self.rserver.set(result['job_id'], json.dumps(result['records']), ex=self.cache['greynoise'])
        return result
    
    def virustotal(self):
        result = self.check_cache('virustotal',  self.kwargs['md5'])
        if not result['records']:
            url = '{}?apikey={}&resource={}'.format(api_keys['virustotal']['url'], api_keys['virustotal']['key'], self.kwargs['md5'])
            virustotal = requests.get(url).json()
            result['records'] = [virustotal] if virustotal['response_code'] == 1 else []
            self.rserver.set(result['job_id'], json.dumps(result['records']), ex=self.cache['virustotal'])
        return result

    def xforce(self):
        result = self.check_cache('xforce',  self.kwargs['md5'])
        if not result['records']:
            url = '{}/malware/{}'.format(api_keys['xforce']['url'], self.kwargs['md5'])
            xforce = requests.get(url, auth=(api_keys['xforce']['key'], api_keys['xforce']['password'])).json()
            result['records'] = [xforce] if not 'error' in xforce else []
            self.rserver.set(result['job_id'], json.dumps(result['records']), ex=self.cache['xforce'])
        return result


class Producer:
    def __init__(self, server='localhost:9092', **kwargs):
        self.kwargs = kwargs
        self.producer = KafkaProducer(bootstrap_servers=server,
            value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    
    def produce_enrichment(self, key, value, records):
        for record in records:
            record[key] = value
            self.producer.send(self.kwargs['topic'], record).get(timeout=10)

    def greynoise(self):            
        all_ips = ContextES().get_unique_extips()
        for ip in all_ips:
            records = Intel(ip=ip).greynoise()['records']
            produce_records = self.produce_enrichment('src_ip', ip, records)
    
    def virustotal(self):            
        all_indicators = ContextFile().get_indicators()
        for indicator in all_indicators:
            records = Intel(md5=indicator).virustotal()['records']
            produce_records = self.produce_enrichment('md5', indicator, records)

    def xforce(self):
        all_indicators = ContextFile().get_indicators()
        for indicator in all_indicators:
            records = Intel(md5=indicator).xforce()['records']
            produce_records = self.produce_enrichment('md5', indicator, records)
            
# Producer(topic='intel-xforce').xforce()
