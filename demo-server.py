# -*- coding: utf-8 -*-
"""
Author:        Wang Chao <yueyoum@gmail.com>
Filename:      demo-server.py
Date created:  2015-02-19 14:27:18
Description:

"""

import json

from islands.process import Process
from islands.process import pm


class MyProcess(Process):
    def handler_transport(self, data):
        print "MyProcess: handler_transport", data
        data = json.loads(data)
        cmd = data['cmd']
        transport_handler = "handler_transport_%s" % cmd
        handler = getattr(self, transport_handler)
        handler(data)

    def handler_transport_login(self, data):
        pid = data['pid']
        self.got_pid(pid)

    def handler_transport_chat_global(self, data):
        pm.send_to_all(data['text'], exclude_pid=self.pid)

    def handler_test(self, data):
        print "MyProcess: handler_test", data


    def on_terminate(self):
        super(MyProcess, self).on_terminate()
        print "MyProcess: on_terminate"


