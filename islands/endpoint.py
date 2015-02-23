# -*- coding: utf-8 -*-
"""
Author:        Wang Chao <yueyoum@gmail.com>
Filename:      endpoint.py
Date created:  2015-02-19 13:00:28
Description:

"""

import gevent
from gevent.queue import Queue

from socket import error as socket_error

from islands.stream import StreamMixin

class EndPoint(gevent.Greenlet, StreamMixin):
    def __init__(self, transport):
        gevent.Greenlet.__init__(self)

        self.transport = transport
        self.mailbox = Queue()
        self.jobs = []

        print "EndPoint new"

    def put(self, data):
        self.mailbox.put(data)


    def recv_from_transport(self):
        try:
            while True:
                length = self.transport.recv(4)
                if not length:
                    self.on_connection_closed()
                    break

                length = StreamMixin.FMT_HEADER.unpack(length)[0]
                data = self.transport.recv(length)
                assert len(data) == length
                print "EndPoint: recv", data
                self.put(('transport', data))
        except socket_error:
            pass
        except AssertionError:
            pass


    def send_to_transport(self, data):
        binary = self.SerializeToString(data)
        self.transport.sendall(binary)


    def on_connection_closed(self):
        """called when closed the connection"""
        print "EndPoint connection closed by remote"
        pass


    def on_terminate(self):
        """called when before kill this greenlet"""
        pass


    def terminate(self, *args):
        print "EndPoin terminate"
        for job in self.jobs:
            job.unlink(self.terminate)

        gevent.killall(self.jobs)
        self.transport.close()
        self.on_terminate()
        self.kill()


    def _run(self):
        job_recv = gevent.spawn(self.recv_from_transport)
        self.jobs.append(job_recv)

        for job in self.jobs:
            job.link(self.terminate)

        gevent.joinall(self.jobs)


