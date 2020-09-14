#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Wylie Standage-Beier.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy as np

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

