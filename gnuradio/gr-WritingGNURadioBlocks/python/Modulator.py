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
from config import constilation, bits_per_symbol

class Modulator(gr.decim_block):
    ''' '''

    def __init__(self, constilation=constilation, bits_per_symbol=bits_per_symbol):
        gr.decim_block.__init__(
            self, name='Modulator',
            in_sig=[np.int8], out_sig=[np.complex64],
            decim=bits_per_symbol)
        self.constilation, self.bits_per_symbol = constilation, bits_per_symbol

    def work(self, input_items, output_items):
        ''' '''
        in0, out = input_items[0], output_items[0]
        in0 = np.reshape(in0[:len(in0)//self.bits_per_symbol*self.bits_per_symbol],
                         (-1, 2))  # force input buffer is even
        out[:] = np.array([self.constilation[tuple(b)] for b in in0]).flatten()
        return len(in0)//self.bits_per_symbol


