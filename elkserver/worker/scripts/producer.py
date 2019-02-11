from kafka import KafkaProducer
from intelligence import ContextES
from intelligence import ContextFile
from intelligence import Intel
import json


class IntelProducer:
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
    
    def hybridanalysis(self):
        all_indicators = ContextFile().get_indicators()
        records = Intel(md5=all_indicators).hybridanalysis()['records']
        for indicator in records:
            produce_records = self.produce_enrichment('md5', indicator['md5'], [indicator])
            

# Producer(topic='intel-hybridanalysis').hybridanalysis()
