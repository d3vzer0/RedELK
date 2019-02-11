from kafka import KafkaConsumer, KafkaProducer
from enrichment import Lookups
import json
import re

class Enrich:
    def __init__(self, enrichers, data):
        self.enrichers = enrichers
        self.data = data
        
    def multi(self, enricher_type, result=False):
        enricher = self.enrichers[enricher_type]['lookups']
        for compare in enricher:
            match_hostname = compare['target_hostname'].match(self.data['target_hostname'])
            match_ipint = compare['target_ipint'].match(self.data['target_ipint'])
            match_user = compare['target_user'].match(self.data['target_user'])
            if (compare['query_mode'] == 'AND' and (match_hostname and match_ipint and match_user)):
                return True
            if (compare['query_mode'] == 'OR' and (match_hostname or match_ipint or match_user)):
                return True
        return result
    
    def single(self, enricher_type, field, result=False):
        if self.data[field] in self.enrichers[enricher_type]['lookups']:
            result = True
        return result

    def new_beacon(self, enrich_result={}):
        for enricher, value in self.enrichers.items():
            match_lookup = self.multi(enricher) if value['type'] == 'multi' else self.single(enricher, value['field'])
            enrich_result[enricher] = match_lookup
        return {**self.data, **{'matches':enrich_result}}


class EnrichProducer:
    def __init__(self, server='localhost:9092', topic='cobaltstrike-newbeacons-enriched'):
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=server,
            value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    def produce(self, data):
        self.producer.send(self.topic, data).get(timeout=10)
        

class EnrichConsumer:
    def __init__(self, server='localhost:9092'):
        self.enrichers = Lookups().load()
        self.producer = EnrichProducer()
        self.consumer = KafkaConsumer('cobaltstrike-newbeacons-logstash',
            group_id='consumer-newbeacons-enricher',
            bootstrap_servers=[server],
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('ascii')))

    def consume(self):
        for message in self.consumer:
            message_content = message.value
            enrich_beacon = Enrich(self.enrichers, message_content).new_beacon()
            self.producer.produce(enrich_beacon)

if __name__ == '__main__':
    EnrichConsumer().consume()