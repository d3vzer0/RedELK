from elasticsearch import Elasticsearch
from variables import config
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
        self.es = Elasticsearch([config['elasticsearch']['host']])
        self.beacon_index = "beacondb-enriched*"
        self.rtops_index = "cobaltstrike-*"

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
