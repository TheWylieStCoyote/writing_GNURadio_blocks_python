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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from BitErrorCounter import BitErrorCounter


class qa_BitErrorCounter(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001(self):
        bits = [0, 0, 1, 1, 0, 1, 1, 0]
        src0 = blocks.vector_source_b(bits)
        src1 = blocks.vector_source_b(bits)
        bec = BitErrorCounter()
        self.tb.connect((src0, 0), (bec, 0))
        self.tb.connect((src1, 0), (bec, 1))
        self.tb.run()
        ber = bec.get_BER()
        print(f'BER {ber}')

    def test_002(self):
        bits0 = [0, 0, 1, 1, 0, 1, 1, 0]
        bits1 = [0, 0, 1, 1, 1, 1, 1, 0]
        src0 = blocks.vector_source_b(bits0)
        src1 = blocks.vector_source_b(bits1)
        bec = BitErrorCounter()
        self.tb.connect((src0, 0), (bec, 0))
        self.tb.connect((src1, 0), (bec, 1))
        self.tb.run()
        ber = bec.get_BER()
        print(f'BER {ber}')

    def test_003(self):
        bits0 = [0, 0, 1, 1, 0, 1, 1, 0]
        bits1 = [1, 1, 0, 0, 1, 0, 0, 1]
        src0 = blocks.vector_source_b(bits0)
        src1 = blocks.vector_source_b(bits1)
        bec = BitErrorCounter()
        self.tb.connect((src0, 0), (bec, 0))
        self.tb.connect((src1, 0), (bec, 1))
        self.tb.run()
        ber = bec.get_BER()
        print(f'BER {ber}')


if __name__ == '__main__':
    gr_unittest.run(qa_BitErrorCounter)
