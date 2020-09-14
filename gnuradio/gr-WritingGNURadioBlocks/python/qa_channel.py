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
from channel import Channel


class qa_channel(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001(self):
        src = blocks.vector_source_c(np.zeros(10))
        channel = Channel(snr=10)
        dst = blocks.vector_sink_c()
        self.tb.connect(src, channel)
        self.tb.connect(channel, dst)
        self.tb.run()
        results_data = dst.data()

if __name__ == '__main__':
    gr_unittest.run(qa_channel)
