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

class Demodulator(gr.interp_block):
    ''' '''

    def __init__(self, constilation=constilation, bits_per_symbol=bits_per_symbol):
        ''' '''
        gr.interp_block.__init__(
            self, name='Demodulator',
            in_sig=[np.complex64], out_sig=[np.int8],
            interp=bits_per_symbol)
        self.constilation, self.bits_per_symbol = constilation, bits_per_symbol
        self.constilation_points = np.array(list(constilation.values())).reshape((1, -1))
        self.bit_combinations = np.array(list(constilation.keys())).reshape((-1, bits_per_symbol))

    def work(self, input_items, output_items):
        ''' '''
        in0, out = np.reshape(input_items[0], (-1, 1)), output_items[0]
        length = len(in0)*self.bits_per_symbol
        out[:length] = np.reshape(self.bit_combinations[np.argmin(
            np.abs(in0-self.constilation_points),
            axis=1)], (-1,))
        return length


