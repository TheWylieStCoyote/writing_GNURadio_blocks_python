#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Wylie Standage-Beier.
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


import numpy as np
from gnuradio import gr


def apply_channel(signal, snr):
    ''' adds white noise to signal '''
    noise = (np.random.randn(N) + 1j*np.random.randn(N))/(np.sqrt(2)*snr)
    return signal + noise


class Channel(gr.sync_block):
    ''' '''

    def __init__(self, snr):
        ''' '''
        gr.sync_block.__init__(
            self, name='AWGN Channel',
            in_sig=[np.complex64], out_sig=[np.complex64])
        self.snr = snr

    def work(self, input_items, output_items):
        ''' '''
        in0, out = input_items[0], output_items[0]
        length = len(in0)
        noise = (np.random.randn(length)+1j*np.random.randn(length))/(self.snr*np.sqrt(2))
        out[:] = in0+noise
        return length

    def get_snr(self):
        ''' '''
        return self.snr

    def set_snr(self, snr):
        ''' '''
        self.snr = snr

