import numpy as np
from Globals import *


class Spectrum:
    def __init__(self):
        self.x_f = []  # frequencies (x-axis)
        self.f_hat = []  # FFT result (complex numbers)
        self.psd = []  # Power Spectral Density
        self.f_abs = []  # Normalized FFT result
        self.fs = SAMPLE_RATE
        self.n = 0
        self.parent_signal = None

    def get_peaks(self, in_db=False, reference_amp=1):
        x, y = self.get_usable_range(in_db=in_db, reference_amp=reference_amp)
        peaks = list(zip(y, x))
        peaks.sort(reverse=True)
        return peaks

    def get_usable_range(self, in_db=False, reference_amp=1):
        # usable range (Nyquist theorem)
        usable_range = np.arange(1, np.floor(self.n / 2), dtype='int')
        frequencies = self.x_f[usable_range]
        freq_levels = self.f_abs[usable_range]
        if in_db:
            freq_levels = 20 * np.log10(freq_levels/reference_amp)
        return frequencies, freq_levels
