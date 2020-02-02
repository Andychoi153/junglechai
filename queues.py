import hashlib
from multiprocessing import Manager

enc = hashlib.md5()

iron = Manager().Queue()
bronze = Manager().Queue()
silver = Manager().Queue()
gold = Manager().Queue()
platinum = Manager().Queue()
diamond = Manager().Queue()
master = Manager().Queue()
grand_master = Manager().Queue()
challenger = Manager().Queue()

queues = [
    iron,
    bronze,
    silver,
    gold,
    platinum,
    diamond,
    master,
    grand_master,
    challenger
]

matches = Manager().dict({})


def dequeueing(queues, match):
    try:
        while True:
            for pair in queues:
                if pair.qsize() >= 2:
                    a = pair.get()
                    b = pair.get()
                    # random hash
                    string = (a+b).encode('utf-8')
                    enc.update(string)
                    hashing_chat_room = enc.hexdigest()
                    matches.update({a: {
                                          'room': hashing_chat_room,
                                          'duo': b},
                                    b: {
                                            'room': hashing_chat_room,
                                            'duo': a}})

                    print('hashing done')

    except Exception as e:
        print('whats?')
        print(e)
        while True:
            for pair in queues:
                if pair.qsize() >= 2:
                    a = pair.get()
                    b = pair.get()
                    # random hash
                    string = (a+b).encode('utf-8')
                    enc.update(string)
                    hashing_chat_room = enc.hexdigest()
                    matches.update({a: hashing_chat_room,
                                    b: hashing_chat_room})
                    print('hashing done')
