# -*- coding: utf-8 -*-
"""
Author:        Wang Chao <yueyoum@gmail.com>
Filename:      demo-client.py
Date created:  2015-02-19 16:18:58
Description:

"""

import json

import random
import gevent
from gevent import socket

from islands.stream import StreamMixin


def client(cid):
    s = socket.socket()
    s.connect(('127.0.0.1', 9090))

    data = {
            'cmd': 'login',
            'pid': cid,
            }

    binary = StreamMixin().SerializeToString(json.dumps(data))
    s.send(binary)

    gevent.sleep(random.randint(1, 3))

    data = {
            'cmd': 'chat_global',
            'text': '你好，来自{0}'.format(cid)
            }

    binary = StreamMixin().SerializeToString(json.dumps(data))
    s.send(binary)

    gevent.sleep(random.randint(5, 8))

    data = s.recv(100)
    print "{0} GOT DATA {1}".format(cid, data)

    s.close()

for i in range(10):
    gevent.spawn(client, i)


gevent.wait()





