import numpy as np
from scipy.signal import chirp
from archive_2 import utils_calc as calc
import utils_plt as plt
from AudioController import AudioController as usd
from Signal import Signal
from Spectrum import Spectrum
from scipy.interpolate import *
from scipy.signal import butter, sosfilt


def get_base_signals(duration, frequency_distribution):
    signals = []
    for frequency in frequency_distribution:
        model_signal = Signal(f=frequency, d=duration)
        model_signal.generate_sine()
        signals.append(model_signal)
    return signals


def get_chirp_signal(duration):
    signals = []
    model_signal = Signal(d=duration)
    model_signal.y = chirp(t=model_signal.t, f0=1, f1=20000,
                           t1=model_signal.t[len(model_signal.t)-1],
                           method='logarithmic', phi=90)
    # model_signal.apply_windowing()
    signals.append(model_signal)
    # plt.plt.plot(model_signal.t, model_signal.y)
    return signals


def get_recorded_signals(base_signals):
    recorded_signals = []
    for base_signal in base_signals:
        sample = usd.record_sample(base_signal)
        recorded_signal = Signal(y=sample, f=base_signal.f, d=base_signal.d)
        recorded_signals.append(recorded_signal)
    return recorded_signals


def plot_data(*signals):
    # if len(signals) == 1 and len(signals[0]) > 1:
    #    signals = signals[0]
    for signal in signals:
        if isinstance(signal, Signal):
            plt.plot_time_signal(signal)
        elif isinstance(signal, Spectrum):
            plt.plot_frequency_domain_signal(signal)





def apply_gain(data, gain=0):
    if gain == 0:
        return data
    else:
        return data * 10**(gain/20)


def bandpass_filter(data, fc, bandwidth, fs, order=6):
    low = fc/2**(bandwidth/2)
    high = fc*2**(bandwidth/2)
    if high > fs/2:
        high = fs/2 - 1
    sos = butter(N=order, Wn=[low, high], btype='bandpass', analog=False, fs=fs, output='sos')
    filtered = sosfilt(sos, data)
    return filtered


def lowpass_filter(data, cutoff, fs, order=1):
    sos = butter(N=order, Wn=cutoff, btype='lowpass', analog=False, fs=fs, output='sos')
    return sosfilt(sos, data)


def highpass_filter(data, cutoff, fs, order=1):
    sos = butter(N=order, Wn=cutoff, btype='highpass', analog=False, fs=fs, output='sos')
    return sosfilt(sos, data)


def eq(data, frequencies, bandwidth=1/3, apply_only_bandpass=False):
    equalized = None
    i = 1
    for f in frequencies:
        if i == 1 and apply_only_bandpass is False:
            filtered = apply_gain(gain=0, data=lowpass_filter(data, f*(2**(bandwidth/2)), 44100, 6))
        elif i == len(frequencies) and apply_only_bandpass is False:
            filtered = apply_gain(gain=0, data=highpass_filter(data, f/(2**(bandwidth/2)), 44100, 6))
        else:
            filtered = apply_gain(gain=0, data=bandpass_filter(data, f, bandwidth, 44100, 6))
        if equalized is None:
            equalized = filtered
        else:
            equalized += filtered
        i += 1
    return equalized


def interpolate_fft(fft, frequencies):
    x, y = fft.get_usable_range(in_db=True, reference_amp=0.01)
    f_peaks = []
    y_peaks = []

    for frequency in frequencies:
        j = int(round(frequency, 0) - 1)
        print("frequency: ", frequency)
        print(y[j - 1])
        print(y[j])
        print(y[j + 1])
        f_peaks.append(j + 1)
        y_peaks.append(y[j])

    # temporary solution for low and high
    low = 20
    high = 20000
    x_new = np.arange(low, high + 1, 1)

    simple_inter = interp1d(f_peaks, y_peaks, 'linear')
    cubic_spline = interp1d(f_peaks, y_peaks, 'cubic')  # CubicSpline(f_peaks, y_peaks)

    y1_simple = simple_inter(x_new)
    y1_cubic = cubic_spline(x_new)
    plt.adhoc_plot_frequency_domain_signal(x_new, y1_simple, "simple interpolation, only peaks")
    plt.adhoc_plot_frequency_domain_signal(x_new, y1_cubic, "cubic spline interpolation, only peaks")

    # x_new - wszystkie częstotliwości
    # y1_cubic - interpolacja za pomocą Cubic Spline
    # threshold - założenie jakiegoś poziomu db, do którego dążymy
    """threshold = -25.0

    y2_threshold = y1_cubic
    i = 0
    for y in y1_cubic:
        y2_threshold[i] = (-1 * y) + threshold  # symmetry against axis X + coefficient B
        i += 1

    plt.adhoc_plot_frequency_domain_signal(x_new, y2_threshold,
                                           "gain difference against -25db, cubic spline interpolation, only peaks")"""


def swipe_through_frequencies(steps=100, duration=2):
    sigs = []
    ffts = []
    rec_sigs = []
    rec_ffts = []
    for frequency in calc.get_frequency_distribution(steps=steps):
        model_signal = Signal(f=frequency, d=duration)
        model_signal.generate_sine()
        '''
        model_fft = SignalInFrequencyDomain()
        model_fft.transform_time_domain_signal(model_signal)

        sigs.append(model_signal)
        ffts.append(model_fft)

        sample = usd.record_sample(model_signal)
        recorded_signal = SignalInTimeDomain(y=sample, f=frequency, d=duration)
        recorded_fft = recorded_signal.get_frequency_representation()

        rec_sigs.append(recorded_signal)
        rec_ffts.append(recorded_fft)
        '''
        # plot_results(model_signal, model_fft, recorded_signal, recorded_fft)

    white = 0.05 * np.random.randn(44100)
    temp = Signal(y=white, fs=44100, d=1)
    temp.prepare_x_axis()
    temp.apply_windowing()
    sigs.append(temp)
    summary_sig = calc.sum_signals(sigs)
    summary_fft = summary_sig.get_frequency_representation()

    import copy as cp
    summary_fft_2 = cp.deepcopy(summary_fft)
    summary_fft_2.f_abs = 20 * np.log10(summary_fft_2.f_abs)
    '''
    summary_rec_sig = calc.sum_signals(rec_sigs)
    summary_rec_fft = summary_rec_sig.get_frequency_representation()

    summary_rec_fft_2 = calc.sum_ffts(rec_ffts)

    summary_rec_fft_2.f_abs = 20 * np.log10(summary_rec_fft_2.f_abs)
    '''

    fft_clean_up = cp.deepcopy(summary_fft)
    y = fft_clean_up.f_abs[fft_clean_up.f_abs > 0.05 * max(fft_clean_up.f_abs)]
    x = fft_clean_up.x_f[fft_clean_up.f_abs > 0.05 * max(fft_clean_up.f_abs)]
    fft_clean_up.f_abs = y
    fft_clean_up.x_f = x
    plt.plot_results(summary_sig, summary_fft, summary_sig, fft_clean_up)
