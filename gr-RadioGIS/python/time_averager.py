#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 RadioGIS.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
import time
from gnuradio import gr


class time_averager(gr.sync_block):
    """
    Average for t seconds
    """
    def __init__(self, N, t=300):
        self.N = N
        self.l = time.time() + t
        self.t = t
        self.num = 0
        self.output = numpy.zeros([2 * numpy.dtype(numpy.float32).itemsize, N])
        gr.sync_block.__init__(self,
            name="time_averager",
            in_sig=[(numpy.float32, self.N)],
            out_sig=[(numpy.float32, self.N)])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        if time.time() < self.l:
            try:
                self.output[:in0.shape[0], :] += in0
                self.num += 1
            except:
                pass
            out[:] = 0
        else:
            out[:] = self.output[:out.shape[0], :] / self.num
            self.l += self.t
            self.num = 0
            self.output = numpy.zeros([2 * numpy.dtype(numpy.float32).itemsize, self.N])

        out[:] = numpy.average(out, 0)
        
        return len(output_items[0])

