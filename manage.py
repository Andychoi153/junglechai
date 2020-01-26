#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from multiprocessing import Process
# from queues import matches, dequeueing, queues

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
                    string = (a + b).encode('utf-8')
                    enc.update(string)
                    hashing_chat_room = enc.hexdigest()
                    matches.update({a: hashing_chat_room,
                                    b: hashing_chat_room})
                    print('hashing done')

    except Exception as e:
        print('whats?')
        print(e)



def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

    try:
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # if sys.argv[0] != 'collectstatic':

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    p = Process(target=dequeueing, args=(queues, matches), daemon=True)
    p.start()
    main()
