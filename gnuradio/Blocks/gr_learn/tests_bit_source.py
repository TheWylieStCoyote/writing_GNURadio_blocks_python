

import numpy as np
from gnuradio import gr, blocks, gr_unittest
from matplotlib import pyplot as plt
from time import sleep


N = 1_000  # Number of samples
averages = 100  # The number of averages
M = 4    # Symbol order
bits_per_symbol = int(np.log2(M))
number_of_bits = bits_per_symbol * N
bit_combinations = np.array([(0, 0), (0, 1), (1, 0), (1, 1)], dtype=np.bool)
constilation_points = np.array([1+1j, -1+1j, -1-1j, 1-1j])/np.sqrt(2)
constilation = {tuple(b): p
                for b, p in zip(bit_combinations, constilation_points)}


class BitSource(gr.sync_block):
    ''' '''

    def __init__(self, bits_per_symbol=2, N=512):
        ''' '''
        gr.sync_block.__init__(
            self, name='BitSource',
            in_sig=None, out_sig=[(np.int8, bits_per_symbol)])
        self.N, self.bits_per_symbol = N, bits_per_symbol

    def work(self, input_items, output_items):
        ''' '''
        out = output_items[0]
        length = len(out)
        # out[:] = np.random.randn((self.N, self.bits_per_symbol)) > 0
        out[:] = np.random.randint(
            low=0, high=2, size=(length, self.bits_per_symbol), dtype=np.int8)
        return length


class qa_random_bit_source(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001(self):
        bs = BitSource()
        head = blocks.head(2, 100)
        dst = blocks.vector_sink_b(vlen=2)
        self.tb.connect(bs, head)
        self.tb.connect(head, dst)
        self.tb.run()
        results_data = dst.data()
        print(results_data)


if __name__ == '__main__':
    gr_unittest.run(qa_random_bit_source)
