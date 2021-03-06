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

import consumer
import numpy
import time
from datetime import datetime, timedelta
from gnuradio import gr

class data_submitter(gr.sync_block):
    """
    docstring for block data_submitter
    """
    def __init__(self, N, gps):
        self.N = N
        self.gps = gps
        gr.sync_block.__init__(self,
            name="data_submitter",
            in_sig=[(numpy.float32, self.N)],
            out_sig=None)
     
    def split_pos(self):
        pos = self.gps.split()
        lat, lon = pos[1], pos[3]
        return float(lon), float(lat)

    def set_gps(self, gps):
        self.gps = gps

    def work(self, input_items, output_items):
        in0 = input_items[0].astype("string")
        data = ""

        for x in in0:
            data += " ".join(x)
            data += ";"

        data = data[:-2]

        date = datetime.utcnow() - timedelta(hours=5) #COT Bogota, -5 UTC
        date = date.strftime('%d/%m/%Y %H:%M:%S')
        time.sleep(2)
        server = "http://radiogis.uis.edu.co/sensores/medidas"

        lat, lon = self.split_pos()
        print lat, lon, date
        consumer.send_raw(date, 1, data, 2, 3, lat, lon, 27, url=server)


        return len(input_items[0])

