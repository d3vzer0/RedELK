from elasticsearch import Elasticsearch
from kafka import KafkaProducer
import json
import requests

class Context:
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
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.greynoise_url = 'http://api.greynoise.io:8888/v1/query/ip'
        self.vt_url = 'https://www.virustotal.com/vtapi/v2/file/report'

    def greynoise(self):
        greynoise = requests.post(self.greynoise_url, data={'ip':self.kwargs['ip']}).json()
        records = greynoise.get('records', [])
        return records
    
    def virustotal(self):
        return None


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
        all_ips = Context().get_unique_extips()
        for ip in all_ips:
            records = Intel(ip=ip).greynoise()
            produce_records = self.produce_enrichment('src_ip', ip, records)

        

    


Producer('192.168.1.124:9092', topic='intel-greynoise').greynoise()
