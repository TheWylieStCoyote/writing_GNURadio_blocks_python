

import numpy as np
from gnuradio import gr, blocks, gr_unittest


class BitSource(gr.sync_block):
    ''' '''

    def __init__(self):
        ''' '''
        gr.sync_block.__init__(
            self, name='BitSource',
            in_sig=None, out_sig=[(np.int8)])

    def work(self, input_items, output_items):
        ''' '''
        out = output_items[0]
        length = len(out)
        out[:] = np.random.randint(
            low=0, high=2, size=length, dtype=np.int8)
        return length


class qa_random_bit_source(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001(self):
        bs = BitSource()
        head = blocks.head(1, 100)
        dst = blocks.vector_sink_b()
        self.tb.connect(bs, head)
        self.tb.connect(head, dst)
        self.tb.run()
        results_data = dst.data()


if __name__ == '__main__':
    gr_unittest.run(qa_random_bit_source)
