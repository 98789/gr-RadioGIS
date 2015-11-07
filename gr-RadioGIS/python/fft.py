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

class fft(gr.sync_block):
    """
    Perform fft
    """
    def __init__(self, N, W, window):
        self.N = N
        self.W = getattr(self, W)
        self.window = window
        gr.sync_block.__init__(self,
            name="fft",
            in_sig=[(numpy.complex64, self.N)],
            out_sig=[(numpy.complex64, self.N)])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        N_min = min(self.N, 2)
    
        n = numpy.arange(N_min)
        k = n[:, None]
        M = self.W(n*k, N_min)

        for i, x in enumerate(in0):

            X = numpy.dot(M, x.reshape((N_min, -1)))

            while X.shape[0] < self.N:
                X_even = X[:, :X.shape[1] / 2]
                X_odd = X[:, X.shape[1] / 2:]
                factor = self.W(numpy.arange(X.shape[0]), X.shape[0]*2)[:, None]
                X = numpy.vstack([X_even + factor * X_odd,
                       X_even - factor * X_odd])

            X=X.ravel()
            Y = numpy.hstack([X[self.N/2:],X[:self.N/2]])
            out[i][:] = Y

        return len(output_items[0])

    def set_window(self, window):
        self.window = window

    def set_W(self, W):
        self.W = getattr(self, W)

    def exponencial(self, nk, N):
        """exponential weight"""
        W = numpy.exp(-2j * numpy.pi * nk / N)

        return W

    def triangular(self, nk, N):
        """triangular weight"""

        nk %= N
        W = 2 * abs( 2.0 * nk / N - 1) - 1 + 0j
        W += (1 - abs(4.0 * nk / N - 1)) * 1j
        W[nk >= N/2] = W[nk >= N/2].conjugate()

        return W

    def potencia(self, nk, N):
        """Power weight"""

        nk %= N
        L = (1 - 4.0 * nk / N)
        L[nk >= N/2] = L[nk >= N/2] * -1 - 2
        W = L * (2 - abs(L)) + 0j
        W += (1 - L * L) * 1j
        W[nk >= N/2] = W[nk >= N/2].conjugate()

        return W

    def binomial(self, nk, N):
        """Binomial weight"""

        nk %= N
        L = (N / 4.0 - nk)
        L[nk >= N/2] = L[nk >= N/2] * -1 - N / 2.0
        A = N * (N / 4.0 + 1) / 4
        W = L * (N / 2.0 + 1 - abs(L)) / A + 0j
        W += ((A - abs(L) * (abs(L) + 1)) / A) * 1j
        W[nk >= N/2] = W[nk >= N/2].conjugate()

        return W
