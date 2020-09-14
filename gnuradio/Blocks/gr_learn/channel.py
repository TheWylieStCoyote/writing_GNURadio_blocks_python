
import numpy as np
from gnuradio import gr, blocks, gr_unittest


def apply_channel(signal, snr):
    ''' adds white noise to signal '''
    noise = (np.random.randn(N) + 1j*np.random.randn(N))/(np.sqrt(2)*snr)
    return signal + noise


class AwgnChannel(gr.sync_block):
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


class qa_channel(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001(self):
        src = blocks.vector_source_c(np.zeros(10))
        channel = AwgnChannel(snr=10)
        dst = blocks.vector_sink_c()
        self.tb.connect(src, channel)
        self.tb.connect(channel, dst)
        self.tb.run()
        results_data = dst.data()


if __name__ == '__main__':
    gr_unittest.run(qa_channel)
