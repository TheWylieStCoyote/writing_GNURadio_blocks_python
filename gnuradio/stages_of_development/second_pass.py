
import numpy as np
from matplotlib import pyplot as plt

N = 1_000  # Number of samples
M = 4    # Symbol order
bits_per_symbol = int(np.log2(M))
number_of_bits = bits_per_symbol * N
bit_combinations = np.array([(0, 0), (0, 1), (1, 0), (1, 1)], dtype=np.bool)
constilation_points = np.array([1+1j, -1+1j, -1-1j, 1-1j])/np.sqrt(2)
constilation = {tuple(b): p
                for b, p in zip(bit_combinations, constilation_points)}

SNRdB = np.arange(-20, 20, 1)
SNR = 10**(np.array(SNRdB)/20)


def generate_bits(M, N):
    return np.random.randn(N, bits_per_symbol) > 0


def modulate_bits(bits, constilation=constilation):
    return np.array([constilation[tuple(b)] for b in bits])


def apply_channel(signal, snr):
    noise = (np.random.randn(N) + 1j*np.random.randn(N))/(np.sqrt(2)*snr)
    return signal + noise


def demodulate_signal(signal, constilation=constilation):
    return bit_combinations[np.argmin(
        np.abs(received_signal.reshape(N, 1)-constilation_points.reshape((1, M))),
        axis=1)]


def compute_bit_error_rate(source, received):
    number_of_bits = np.size(source)
    return np.sum(np.bitwise_xor(bits, received_bits))/number_of_bits


def plot_ber(SNRdB, ber):
    plt.figure(0, (16, 9))
    plt.semilogy(SNRdB, ber)
    plt.grid(True)
    plt.xlabel('SNR (dB)')
    plt.xlim((min(SNRdB), max(SNRdB)))
    plt.ylabel('Bit Error Rate')
    plt.title(f'{M}-PSK SNR vs BER')
    plt.show()


ber = []

for snr in SNR:
    bits = generate_bits(M, N)
    signal = modulate_bits(bits)
    received_signal = apply_channel(signal, snr)
    received_bits = demodulate_signal(signal)
    ber.append(compute_bit_error_rate(bits, received_bits))


plot_ber(SNRdB, ber)
