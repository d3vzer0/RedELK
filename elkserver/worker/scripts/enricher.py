from kafka import KafkaConsumer

class Enrich:
    def __init__(self, server='localhost:9092', **kwargs):
        self.consumer = KafkaConsumer('cobaltstrike-newbeacons-logstash',
                group_id='consumer-newbeacons-enricher',
                bootstrap_servers=[server],
                auto_offset_reset='earliest')

    def run(self):
        for message in self.consumer:
            print(message)