# -*- coding: utf-8 -*-
"""
Author:        Wang Chao <yueyoum@gmail.com>
Filename:      command.py
Date created:  2015-02-20 20:58:10
Description:

"""
import gevent

import sys
import inspect
import optparse
from islands.process import Process
from islands.process import pm

def run():
    parse = optparse.OptionParser()
    parse.add_option(
            "-p", "--port",
            dest="port",
            type="int",
            help="port to listen"
            )

    parse.add_option(
            "-l", "--logfile",
            dest="logfile",
            help="daemonize"
            )

    options, args = parse.parse_args()

    port = options.port
    logfile = options.logfile

    if not port:
        parse.print_help()
        sys.exit(1)

    module = args[0]

    x = __import__(module.rstrip(".py"))
    for item in dir(x):
        obj = getattr(x, item)

        if inspect.isclass(obj) and obj is not Process and issubclass(obj, Process):
            break
    else:
        raise RuntimeError("No Subclass of Process")

    pm.initialize(port, obj)
    pm.start()

    gevent.wait()

