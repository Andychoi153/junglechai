from kafka import KafkaProducer, KafkaConsumer
from json import dumps, loads


producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         key_serializer=None,
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))


consumer = KafkaConsumer(
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='sr',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

tear_matrix = [
    [1, 0.5, 0.3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # iron
    [0.5, 1, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # bronze
    [0.3, 0.5, 1, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # silver
    [0, 0, 0.5, 1, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0], # gold
    [0, 0, 0, 0.5, 1, 0.8, 0.7, 0, 0, 0, 0, 0, 0, 0], # platinum 4,3
    [0, 0, 0, 0.3, 0.8, 1, 0.8, 0.5, 0, 0, 0, 0, 0, 0], # platinum 2
    [0, 0, 0, 0.3, 0.5, 0.8, 1, 0.5, 0.3, 0, 0, 0, 0, 0],  # platinum 1
    [0, 0, 0, 0, 0, 0.3, 0.5, 1, 0.8, 0.5, 0, 0, 0, 0],  # daia 4
    [0, 0, 0, 0, 0, 0, 0.3, 0.5, 1, 0.8, 0.5, 0, 0, 0],  # daia 3
    [0, 0, 0, 0, 0, 0, 0, 0.3, 0.5, 1, 0.8, 0.5, 0.2, 0],  # daia 2
    [0, 0, 0, 0, 0, 0, 0, 0, 0.3, 0.8, 1, 0.8, 0.5, 0],  # daia 1
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, 0.8, 1, 1, 0.8],  # master
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, 0.8, 1, 1],  # gm
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, 1, 1],  # challenger
]

consumer.subscribe(['test'])
