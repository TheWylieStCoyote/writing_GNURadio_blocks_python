

import numpy as np
from gnuradio import gr, blocks, gr_unittest


bits_per_symbol = 2
bit_combinations = np.array([(0, 0), (0, 1), (1, 0), (1, 1)], dtype=np.bool)
constilation_points = np.array([1+1j, -1+1j, -1-1j, 1-1j])/np.sqrt(2)
constilation = {tuple(b): p
                for b, p in zip(bit_combinations, constilation_points)}


def modulate_bits(bits, constilation=constilation):
    ''' converts bits into symbols '''
    return np.array([constilation[tuple(b)] for b in bits])


def demodulate_signal(signal, constilation=constilation):
    ''' converts signal to best guess of the original bits '''
    return bit_combinations[np.argmin(
        np.abs(np.reshape(signal, (-1, 1))-constilation_points.reshape((1, -1))),
        axis=1)]


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


class qa_modulation_demodulation(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001(self):
        # Test modulation
        bits = np.array([0, 0, 0, 1, 1, 0, 1, 1], dtype=np.int8)
        signal = np.array([1+1j, -1+1j, -1-1j, 1-1j])/np.sqrt(2)
        src = blocks.vector_source_b(bits)
        mod = Modulator()
        dest_signal = blocks.vector_sink_c()
        self.tb.connect(src, mod)
        self.tb.connect(mod, dest_signal)
        self.tb.run()
        gr_signal = dest_signal.data()
        func_signal = modulate_bits(bits.reshape((-1, bits_per_symbol)))
        print(f'Ideal {bits}, {signal}')
        print(f'function {bits}, {func_signal}')
        print(f'block {bits}, {gr_signal}')

    def test_002(self):
        # Test demodulation
        bits = np.array([0, 0, 0, 1, 1, 0, 1, 1], dtype=np.int8)
        signal = np.array([1+1j, -1+1j, -1-1j, 1-1j])/np.sqrt(2)
        src = blocks.vector_source_c(signal)
        demod = Demoulator()
        dest_bits = blocks.vector_sink_b()
        self.tb.connect(src, demod)
        self.tb.connect(demod, dest_bits)
        self.tb.run()
        gr_bits = dest_bits.data()
        func_bits = demodulate_signal(signal)
        print(f'Ideal {bits}')
        print(f'function {func_bits}')
        print(f'block {gr_bits}')

    def test_003(self):
        # Test mouldation and demodulation
        bits = np.array([0, 0, 0, 1, 1, 0, 1, 1], dtype=np.int8)
        expected = np.array([1+1j, -1+1j, -1-1j, 1-1j])/np.sqrt(2)
        src = blocks.vector_source_b(bits)
        mod, demod = Modulator(), Demoulator()
        dest_bits = blocks.vector_sink_b()
        dest_signal = blocks.vector_sink_c()
        tb = gr.top_block()
        tb.connect(src, mod)
        tb.connect(mod, dest_signal)
        tb.connect(mod, demod)
        tb.connect(demod, dest_bits)
        tb.run()
        gr_signal = dest_signal.data()
        func_signal = modulate_bits(bits.reshape((-1, bits_per_symbol)))
        gr_bits = dest_bits.data()
        func_bits = demodulate_signal(func_signal)


if __name__ == '__main__':
    gr_unittest.run(qa_modulation_demodulation)
