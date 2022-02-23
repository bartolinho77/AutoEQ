from Globals import *
from scipy.signal import butter, sosfilt


class Filter:
    @staticmethod
    def band_pass(data, fc, bandwidth, fs=SAMPLE_RATE, order=6):
        low = fc/2**(bandwidth/2)
        high = fc*2**(bandwidth/2)
        if high > fs/2:
            high = fs/2 - 1
        sos = butter(N=order, Wn=[low, high], btype='bandpass', analog=False, fs=fs, output='sos')
        filtered = sosfilt(sos, data)
        return filtered

    @staticmethod
    def low_pass(data, cutoff, fs, order=1):
        sos = butter(N=order, Wn=cutoff, btype='lowpass', analog=False, fs=fs, output='sos')
        return sosfilt(sos, data)

    @staticmethod
    def high_pass(data, cutoff, fs, order=1):
        sos = butter(N=order, Wn=cutoff, btype='highpass', analog=False, fs=fs, output='sos')
        return sosfilt(sos, data)

    @staticmethod
    def apply_gain(data, gain=0):
        if gain == 0:
            return data
        else:
            return data * 10 ** (gain / 20)