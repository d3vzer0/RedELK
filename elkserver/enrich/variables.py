import os

config = {
    'kafka': {
        'host': os.environ['KAFKA_HOST'],
        'group': os.environ['CONSUMER_GROUP'],
        'produce_topic': os.environ['PRODUCER_TOPIC'],
        'consume_topic': os.environ['CONSUMER_TOPIC']
    },
    'elasticsearch': {
        'host': os.environ['ELASTIC_HOST'],
    }
}
