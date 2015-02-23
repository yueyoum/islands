# -*- coding: utf-8 -*-
"""
Author:        Wang Chao <yueyoum@gmail.com>
Filename:      signal.py
Date created:  2015-02-19 19:02:05
Description:

"""

import gevent

class Signal(object):
    def __init__(self):
        self.funcs = []

    def connect(self, func):
        if func not in self.funcs:
            self.funcs.append(func)

        return func

    def send(self, **kwargs):
        for func in self.funcs:
            gevent.spawn(func, **kwargs)


process_new_signal = Signal()
process_pid_signal = Signal()
process_die_signal = Signal()

