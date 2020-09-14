#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Writing GNURadio Blocks
# Author: Wylie Standage-Beier
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import WritingGNURadioBlocks

from gnuradio import qtgui

class WritingGNURadioBlocks(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Writing GNURadio Blocks")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Writing GNURadio Blocks")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "WritingGNURadioBlocks")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.WritingGNURadioBlocks_channel_0 = WritingGNURadioBlocks.channel(1.0)
        self.WritingGNURadioBlocks_bit_source_0 = WritingGNURadioBlocks.bit_source()
        self.WritingGNURadioBlocks_Modulator_0 = WritingGNURadioBlocks.Modulator()
        self.WritingGNURadioBlocks_Demodulator_0 = WritingGNURadioBlocks.Demodulator()
        self.WritingGNURadioBlocks_BitErrorCounter_0 = WritingGNURadioBlocks.BitErrorCounter()



        ##################################################
        # Connections
        ##################################################
        self.connect((self.WritingGNURadioBlocks_Demodulator_0, 0), (self.WritingGNURadioBlocks_BitErrorCounter_0, 0))
        self.connect((self.WritingGNURadioBlocks_Modulator_0, 0), (self.WritingGNURadioBlocks_channel_0, 0))
        self.connect((self.WritingGNURadioBlocks_bit_source_0, 0), (self.WritingGNURadioBlocks_BitErrorCounter_0, 1))
        self.connect((self.WritingGNURadioBlocks_bit_source_0, 0), (self.WritingGNURadioBlocks_Modulator_0, 0))
        self.connect((self.WritingGNURadioBlocks_channel_0, 0), (self.WritingGNURadioBlocks_Demodulator_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "WritingGNURadioBlocks")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate





def main(top_block_cls=WritingGNURadioBlocks, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
