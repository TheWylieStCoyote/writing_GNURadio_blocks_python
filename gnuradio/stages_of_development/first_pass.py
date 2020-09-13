
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


bit_error_rate = []

for snr in SNR:
    # Generate the data to be transmitted
    bits = np.random.randn(N, bits_per_symbol) > 0
    # Modulate the bits to be transmitted
    signal = np.array([constilation[tuple(b)] for b in bits])
    # Generate white noise
    noise = (np.random.randn(N) + 1j*np.random.randn(N))/np.sqrt(2)
    # Apply the AWGN
    received_signal = signal + noise/snr
    # Demodulate the received data
    received_bits = bit_combinations[np.argmin(
        np.abs(received_signal.reshape(N, 1)-constilation_points.reshape((1, M))),
        axis=1)]
    # Compute bit errors
    ber = np.sum(np.bitwise_xor(bits, received_bits))/number_of_bits
    bit_error_rate.append(ber)

# Plot results
plt.figure(0, (16, 9))
plt.semilogy(SNRdB, bit_error_rate)
plt.grid(True)
plt.xlabel('SNR (dB)')
plt.xlim((min(SNRdB), max(SNRdB)))
plt.ylabel('Bit Error Rate')
plt.title(f'{M}-PSK SNR vs BER')
plt.show()
