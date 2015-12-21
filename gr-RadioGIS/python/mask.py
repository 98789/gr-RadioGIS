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
from gnuradio import gr

class mask(gr.sync_block):
    """
    Generate mask
    """
    def __init__(self, x, y, p):
        self.x = x
        self.y = y
        self.p = p
        gr.sync_block.__init__(self,
            name="mask",
            in_sig=None,
            out_sig=[(numpy.float32, self.p)])


    def work(self, input_items, output_items):
        out = output_items[0]

        out[:] = self.get_mask()
        return len(output_items[0])

    def get_mask(self):

        axis = numpy.linspace(self.x[0], self.x[-1], self.p)
        mask = []
        for i in xrange(len(self.x)-1):
            if i < len(self.x) - 2:
                filtered_axis = axis[(axis < self.x[i+1]) & (axis >= self.x[i])]
                numel = filtered_axis.shape[0]
                mask += (numpy.linspace(self.y[i], self.y[i+1], numel, False)).tolist()
            else:
                filtered_axis = axis[(axis <= self.x[i+1]) & (axis >= self.x[i])]
                numel = filtered_axis.shape[0]
                mask += (numpy.linspace(self.y[i], self.y[i+1], numel, True)).tolist()

        return mask

