# -*- coding: utf-8 -*-
"""
Author:        Wang Chao <yueyoum@gmail.com>
Filename:      stream.py
Date created:  2015-02-19 13:01:46
Description:

"""

import struct

class StreamMixin(object):
    FMT_HEADER = struct.Struct('>i')

    def SerializeToString(self, data):
        if isinstance(data, unicode):
            data = data.encode('utf-8')

        length = len(data)
        fmt = '>i%ds' % length
        data_struct = struct.Struct(fmt)
        binary = data_struct.pack(length, data)
        return binary

