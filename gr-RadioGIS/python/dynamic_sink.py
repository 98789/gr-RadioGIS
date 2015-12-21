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


class dynamic_sink(gr.sync_block):
    """
    concatenate n vectors dynamically
    """
    def __init__(self, N, n):
        self.N = N
        self.n = n
        self.last_valid = 0
        gr.sync_block.__init__(self,
            name="dynamic_sink",
            in_sig=[(numpy.float32, self.N)],
            out_sig=[(numpy.float32, self.N * self.n)])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        if 0 < abs(numpy.sum(in0)) < 1E300:
            try:
                shape = self.output.shape
                self.output = numpy.hstack([self.output[abs(self.output) < 1E300], self.output[abs(self.output) > 1E300]]).reshape(shape)
                self.output[abs(self.output) > 1E300] = 10
            except:
                pass

            if time.time() > self.last_valid + 0.95:
                self.last_valid = time.time()
                try:
                    self.output = numpy.hstack([self.output[:min(in0.shape[0], self.output.shape[0])], in0[:min(in0.shape[0], self.output.shape[0])]])
                except:
                    self.output = in0

                if self.output.shape[1] >= out.shape[1]:
                    self.last_output = self.output
                    self.output = in0

        try:
            out[:self.last_output.shape[0]] = self.last_output
        except:
            try:
                out[:self.output.shape[0]] = numpy.hstack([self.output, numpy.zeros((self.output.shape[0], out.shape[1] - self.output.shape[1]))])
            except:            
                out[:] = 0

        return len(output_items[0])

    def set_n(self, n):
        self.n = n

