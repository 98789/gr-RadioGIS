#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 <+YOU OR YOUR COMPANY+>.
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

class non_zero_file_sink(gr.sync_block):
    """
    docstring for block non_zero_file_sink
    """
    def __init__(self, N, n, File):
        self.N = N
        self.n = n
        self.File = open(File, 'w')
        self.File.write("Started at {0:s} ".format(str(time.time())))
        self.last_valid = 0
        self.banda = 0
        gr.sync_block.__init__(self,
            name="non_zero_file_sink",
            in_sig=[(numpy.float32, self.N)],
            out_sig=None)


    def work(self, input_items, output_items):
        in0 = input_items[0].tolist()
        
        if 0 < abs(numpy.sum(in0)) < 1E300:
            if time.time() > self.last_valid + 0.95:
                if 0 < self.banda <= self.n:
                    self.last_valid = time.time()
                    self.File.write("\n\nBanda {0:s}:\n\n".format(str(self.banda)))
                    self.banda += 1
                    for sub_list in in0:
                        self.File.write(" ".join([str(x) for x in sub_list]))
                        self.File.write("\n")
                else:
                    self.banda = self.banda * self.n + 1
        
        return len(input_items[0])

    def set_File(self, File):
        self.File.close()
        self.File = open(File, 'w')
        self.File.write("Started at {0:s} ".format(str(time.time()))) 
