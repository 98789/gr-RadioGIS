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

class dbm(gr.sync_block):
    """
    convert data to dbm
    """
    def __init__(self):
        self.enabled = True
        gr.sync_block.__init__(self,
            name="dbm",
            in_sig=[numpy.float32],
            out_sig=[numpy.float32])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        if self.enabled:
            out[:] = 20 * numpy.log10(in0) - 30
        else:
            out[:] = in0

        return len(output_items[0])

    def set_enabled(self, status):
        self.enabled = status

