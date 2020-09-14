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


class BitErrorCounter(gr.sync_block):
    ''' '''

    def __init__(self, label=''):
        gr.sync_block.__init__(
            self, name=f'Bit Error Counter {label}',
            in_sig=[np.int8, np.int8],
            out_sig=None)
        self.total, self.errors = 0, 0

    def work(self, input_items, output_items):
        in0, in1 = input_items[0], input_items[1]
        length = min(len(in0), len(in1))
        self.total += length
        self.errors += np.sum(np.logical_xor(in0[:length], in1[:length]))
        return length

    def get_BER(self):
        if self.total == 0:
            return 0
        return self.errors/(self.total)


