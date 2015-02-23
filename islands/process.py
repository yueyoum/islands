# -*- coding: utf-8 -*-
"""
Author:        Wang Chao <yueyoum@gmail.com>
Filename:      process.py
Date created:  2015-02-19 14:05:23
Description:

"""
import gevent
from gevent.server import StreamServer

from islands.endpoint import EndPoint
from islands.signal import (
        process_new_signal,
        process_pid_signal,
        process_die_signal,
        )


class ProcessManager(gevent.Greenlet):
    def __init__(self):
        gevent.Greenlet.__init__(self)
        self.processes = {}
        self.port = None
        self.PC = None

    def initialize(self, port, ProcessClass):
        self.port = port
        self.PC = ProcessClass

    def add_process(self, p):
        self.processes[p.pid] = p
        print "ProcessManager, add_process"
        print self.processes

    def remove_process(self, p):
        try:
            self.processes.pop(p.pid)
        except KeyError:
            print "WARNING: not pid in processes"

        print "ProcessManager, remove_process"
        print self.processes

    def send_to_all(self, data, exclude_pid=None):
        # TODO others nodes
        for p in self.processes.values():
            if p.pid == exclude_pid:
                continue

            p.send_to_transport(data)


    def send(self, pid, data):
        try:
            p = self.processes[pid]
            p.send_to_transport(data)
        except KeyError:
            print "INFO: send to other nodes", pid

    def connection_handler(self, sock, address):
        print "ProcessManager: New client", address
        self.PC.spawn(sock)


    def _run(self):
        s = StreamServer(('0.0.0.0', self.port), self.connection_handler)
        s.serve_forever()

pm = ProcessManager()

@process_pid_signal.connect
def _process_pid(p):
    pm.add_process(p)

@process_die_signal.connect
def _process_die(p):
    pm.remove_process(p)


class Process(EndPoint):
    def __init__(self, transport):
        super(Process, self).__init__(transport)
        process_new_signal.send(p=self)

    def got_pid(self, pid):
        self.pid = pid
        process_pid_signal.send(p=self)

    def get_from_mailbox(self):
        while True:
            tag, data = self.mailbox.get()
            print "Process: get", tag, data
            method_name = 'handler_%s' % tag
            method = getattr(self, method_name)
            method(data)

    def on_terminate(self):
        process_die_signal.send(p=self)

    def _run(self):
        job_mb = gevent.spawn(self.get_from_mailbox)
        self.jobs.append(job_mb)

        super(Process, self)._run()

