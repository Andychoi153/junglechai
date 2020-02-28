from time import sleep
from json import dumps
from kafka import KafkaProducer, KafkaConsumer
import numpy as np
from json import loads
import time
import hashlib
from redis_utils import r
from multiprocessing import Process


enc = hashlib.md5()


producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         key_serializer=None,
                         # batch_size=1,
                         # buffer_memory=1,
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

test_set = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def run_broker():
    for _ in range(100):
        value = np.random.normal(loc=10, scale=20, size=3).astype(str).tolist()

        data = {'누굴지요': {
                    'tear': 13,
                    'tear_matrix': test_set,
                    'time': 0}
                }
        print(data)
        producer.send('match', value=data)
        sleep(0.1)

    print("Consumer 연결")

    topics = consumer.topics()
    print(topics)
    consumer.subscribe(['match'])

    pair = dict()
    match = dict()
    matcher_list = []
    total_match = []
    count = 0
    start = time.time()
    for message in consumer:
        print("topic=%s partition=%d offset=%d: key=%s value=%s" % (message.topic, message.partition,
                                                                    message.offset, message.key,
                                                                    message.value))
        value = message.value
        pair.update(value)
        if count >= 9 or (time.time()-start > 5 and count >= 2):
            sleep(0.5)
            count = -1

            for idx, i in enumerate(pair.items()):
                if i[1].get('delete') == 1:
                    matcher_list.append(i[0])

                if idx != pair.items().__len__():

                    for j in list(pair.items())[idx+1:]:
                        score = i[1].get('tear_matrix')[j[1].get('tear')]
                        if score == 1:
                            match.update({(i[0], j[0]): score})

                        else:
                            if 20 < i[1].get('time') <= 120:
                                if score >= 0.5:
                                    match.update({(i[0], j[0]): score})

                            elif 120 < i[1].get('time'):
                                if score >= 0.3:
                                    match.update({(i[0], j[0]): score})

            # filter 1
            for k, v in match.items():
                if v == 1:
                    if (k[0] not in matcher_list) and (k[1] not in matcher_list):
                        matcher_list.append(k[0])
                        matcher_list.append(k[1])
                        total_match.append(k)

            # filter 0.5
            for k, v in match.items():
                if v >= 0.5:
                    if (k[0] not in matcher_list) and (k[1] not in matcher_list):
                        matcher_list.append(k[0])
                        matcher_list.append(k[1])
                        total_match.append(k)

            # filter 0.3
            for k, v in match.items():
                if v >= 0.3:
                    if (k[0] not in matcher_list) and (k[1] not in matcher_list):
                        matcher_list.append(k[0])
                        matcher_list.append(k[1])
                        total_match.append(k)

            # 매치 된 애들은 match db 에 전송, ttl 은 3초
            for data in total_match:
                # random hash
                string = (data[0] + data[1]).encode('utf-8')
                enc.update(string)
                hashing_chat_room = enc.hexdigest()
                r.hset(data[0], hashing_chat_room, data[1])
                r.hset(data[1], hashing_chat_room, data[0])
                r.expire(data[0], 3)
                r.expire(data[1], 3)

            # pair 에서 match 없는 친구들은 time inc 후 다시 큐에 넣음
            # 여기서는 delete 하지 않음
            for k, v in pair.items():
                if k not in matcher_list:
                    time_value = v.get('time')
                    v.update({'time': time_value+1})
                    producer.send('match', value={k: v})
            # sleep(1)
            pair = dict()
            match = dict()
            matcher_list = []
            total_match = []

        count += 1
        # 표 만들어지면 하면 되지 않나? / blossom algorithm 생각 해볼 것!

if __name__ == '__main__':
    p = Process(target=run_broker, daemon=True)
    p.start()
