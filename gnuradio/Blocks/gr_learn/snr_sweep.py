
import numpy as np
from matplotlib import pyplot as plt
from time import sleep

from flow_graph import TopBlock

SNRdB = np.arange(-20, 20, 1)


def plot_ber(SNRdB, ber):
    ''' Plot the bit error rate '''
    plt.figure(0, (16, 9))
    plt.semilogy(SNRdB, ber)
    plt.grid(True)
    plt.xlabel('SNR (dB)')
    plt.xlim((min(SNRdB), max(SNRdB)))
    plt.ylabel('Bit Error Rate')
    plt.ylim((1e-6, 1))
    plt.title(f'N-PSK SNR vs BER')
    plt.show()


def snr_sweep(SNRdB, duration=3):
    SNR = 10**(np.array(SNRdB)/20)
    tbs = [TopBlock(snr) for snr in SNR]
    for tb in tbs:
        tb.start()
    sleep(duration)
    for tb in tbs:
        tb.stop()
    for tb in tbs:
        tb.wait()
    ber = [tb.biterrors.get_BER() for tb in tbs]
    plot_ber(SNRdB, ber)


if __name__ == '__main__':
    snr_sweep(SNRdB)
