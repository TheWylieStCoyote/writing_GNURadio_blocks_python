

import numpy as np
from gnuradio import gr, blocks
from matplotlib import pyplot as plt
from time import sleep


N = 1_000  # Number of samples
averages = 100  # The number of averages
M = 4    # Number of symbols in the constilation
bits_per_symbol = int(np.log2(M))
number_of_bits = bits_per_symbol * N
bit_combinations = np.array([(0, 0), (0, 1), (1, 0), (1, 1)], dtype=np.bool)
constilation_points = np.array([1+1j, -1+1j, -1-1j, 1-1j])/np.sqrt(2)
constilation = {tuple(b): p
                for b, p in zip(bit_combinations, constilation_points)}


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


class Modulator(gr.decim_block):
    ''' '''

    def __init__(self, constilation=constilation, bits_per_symbol=bits_per_symbol):
        gr.decim_block.__init__(
            self, name='Modulator',
            in_sig=[np.int8], out_sig=[np.complex64],
            decim=bits_per_symbol)
        self.constilation, self.bits_per_symbol = constilation, bits_per_symbol

    def work(self, input_items, output_items):
        ''' '''
        in0, out = input_items[0], output_items[0]
        in0 = np.reshape(in0[:len(in0)//self.bits_per_symbol*self.bits_per_symbol],
                         (-1, 2))  # force input buffer is even
        out[:] = np.array([self.constilation[tuple(b)] for b in in0]).flatten()
        return len(in0)//self.bits_per_symbol


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


class Demoulator(gr.interp_block):
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
        print(f'({self.snr}, {ber})')  # Change print statement


if __name__ == '__main__':  # Add explination
    tb = TopBlock(snr=1)
    tb.start()
    # Let the flow graph run for 1 second
    sleep(1)
    # Stop the flow graph
    tb.stop()
    tb.wait()
    tb.print_bit_error_rate()
