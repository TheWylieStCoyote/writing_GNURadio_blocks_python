

from gnuradio import gr, blocks
from time import sleep

from bit_source import BitSource
from modulation import Modulator, Demoulator
from channel import AwgnChannel
from bit_error_counter import BitErrorCounter


class TopBlock(gr.top_block):
    ''' '''

    def __init__(self, snr):
        ''' '''
        gr.top_block.__init__(self, f'Flow graph {snr}')
        self.snr = snr
        ######################################################################
        # Blocks
        ######################################################################
        self.bitsource = BitSource()
        self.modulator = Modulator()
        self.channel = AwgnChannel(snr)
        self.demodulator = Demoulator()
        self.biterrors = BitErrorCounter()
        ######################################################################
        # Connecting blocks
        ######################################################################
        self.connect((self.bitsource, 0), (self.modulator, 0))
        self.connect((self.modulator, 0), (self.channel, 0))
        self.connect((self.channel, 0), (self.demodulator, 0))
        self.connect((self.demodulator, 0), (self.biterrors, 1))
        self.connect((self.bitsource, 0), (self.biterrors, 0))

        def get_snr(self):
            return self.snr

        def set_snr(self, snr):
            self.snr = snr

        def print_bit_error_rate(self):
            ber = self.biterrors.get_BER()
            print(f'({self.snr}, {ber})')


if __name__ == '__main__':
    tb = TopBlock(snr=1)
    tb.start()
    # Let the flow graph run for 1 second
    sleep(1)
    # Stop the flow graph
    tb.stop()
    tb.wait()
    ber = tb.biterrors.get_BER()
    print(f'BER {ber}')
