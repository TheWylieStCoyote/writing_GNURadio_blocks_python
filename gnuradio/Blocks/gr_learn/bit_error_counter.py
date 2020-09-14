

import numpy as np
from gnuradio import gr, blocks, gr_unittest


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


class qa_random_bit_source(gr_unittest.TestCase):

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
    gr_unittest.run(qa_random_bit_source)
