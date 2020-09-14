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
from gnuradio import gr, gr_unittest
from gnuradio import blocks
from Modulator import Modulator
from Demodulator import Demodulator
from config import modulate_bits, bits_per_symbol, demodulate_signal, modulate_bits

class qa_modulation_demodulation(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001(self):
        # Test demodulation
        bits = np.array([0, 0, 0, 1, 1, 0, 1, 1], dtype=np.int8)
        signal = np.array([1+1j, -1+1j, -1-1j, 1-1j])/np.sqrt(2)
        src = blocks.vector_source_c(signal)
        demod = Demodulator()
        dest_bits = blocks.vector_sink_b()
        self.tb.connect(src, demod)
        self.tb.connect(demod, dest_bits)
        self.tb.run()
        gr_bits = dest_bits.data()
        func_bits = demodulate_signal(signal)
        print(f'Ideal {bits}')
        print(f'function {func_bits}')
        print(f'block {gr_bits}')


if __name__ == '__main__':
    gr_unittest.run(qa_modulation_demodulation)
