from Globals import *
import numpy as np
from copy import deepcopy


class Signal:
    def __init__(self, x=None, y=None, fs=SAMPLE_RATE, d=1, f=-1):
        self.t = x  # x-axis
        self.y = y.squeeze() if y is not None else None  # y-axis
        self.f = f  # frequency; positive for periodic signals; -1 for non-periodic
        self.fs = fs  # sampling frequency
        if y is not None:
            self.d = len(self.y)/self.fs  # duration
        else:
            self.d = d
        self.__evaluate_time__()

    def __add__(self, other):
        if self.fs == other.fs and self.y is not None and other.y is not None and self.d == other.d:
            self.y += other.y
            self.f = -1
            return self
        else:
            raise ValueError("Can't add two signals!")

    def __evaluate_time__(self):
        if self.t is None:
            n = int(self.d * self.fs)
            ts = 1 / self.fs
            self.t = np.linspace(0, (n - 1) * ts, n)

    def __get_applied_windowing__(self):
        sig = np.copy(self.y)
        n = len(self.y)
        sig *= np.hanning(n)
        return sig  # TODO: check how self.y behaves - DOES IT CHANGE?

    def copy(self):
        return deepcopy(self)

    def get_spectrum(self):
        from Spectrum import Spectrum
        # apply windowing
        y = self.__get_applied_windowing__()
        spectrum = Spectrum()
        # get number of samples
        spectrum.n = len(y)
        # prepare vector of frequencies (for x-axis)
        spectrum.x_f = (self.fs / spectrum.n) * np.arange(spectrum.n)
        # compute FFT
        spectrum.f_hat = np.fft.fft(y, spectrum.n)
        # normalize FFT
        spectrum.f_abs = np.abs(spectrum.f_hat) / spectrum.n
        spectrum.f_abs[1:] *= 2
        # compute Power Spectral Density
        spectrum.psd = spectrum.f_hat * np.conj(spectrum.f_hat) / spectrum.n
        spectrum.parent_signal = self
        return spectrum
