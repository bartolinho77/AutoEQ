from Globals import *
from AudioController import AudioController
from Filter import Filter


class AutomaticEq:
    # target_level = dB level to which the final signal level should trend
    def __init__(self, target_level=0, reference_amplitude=1, narrow_bands=False):
        self.target_level = target_level
        self.reference_amplitude = reference_amplitude
        if narrow_bands:
            # default values for narrow-band eq - bandwidth = 1/3 of an octave
            self.__set_center_frequencies__()
            self.bandwidth = 1/3
        else:
            self.__set_center_frequencies__(start=250, end=8000, bandwidth=1)  # 62.5, 20000
            self.bandwidth = 1
        AudioController.choose_default_device(AUDIO_RECORDER, AUDIO_PLAYER)

    def __set_center_frequencies__(self, start=15.625, end=20000, bandwidth=1/3, append_boundaries=False):
        lower_boundary = AUDIO_FREQUENCY_LOWER_BOUNDARY
        upper_boundary = AUDIO_FREQUENCY_UPPER_BOUNDARY
        frequencies = []
        current = start
        while current <= end:
            if lower_boundary <= current <= upper_boundary:
                frequencies.append(current)
            current *= 2 ** bandwidth
        self.center_frequencies = []
        for frequency in frequencies:
            self.center_frequencies.append(round(frequency, 0))
        if append_boundaries:
            self.center_frequencies.insert(0, lower_boundary)
            self.center_frequencies.append(upper_boundary)

    def __evaluate_frequency_response__(self):
        from SignalGenerator import SignalGenerator
        sine_waves = [SignalGenerator.sine(frequency=frequency, amplitude=self.reference_amplitude)
                      for frequency in self.center_frequencies]
        # eq_sine_waves = [self.eq(data=wave) for wave in sine_waves]
        for i in range(len(sine_waves)):
            sine_waves[i].y = self.eq(data=sine_waves[i].y, apply_only_bandpass=True)
        recordings = AudioController.record_signals(sine_waves)
        rec_sum = recordings[0].copy()
        first = True
        for rec in recordings:
            if first:
                first = False
                continue
            else:
                rec_sum += rec
        self.frequency_response = rec_sum.get_spectrum()

    def __evaluate_eq_coefficients__(self, max_step=6):
        if hasattr(self, "coefficients"):
            old_coefficients = self.coefficients.copy()
        peaks = self.frequency_response.get_peaks(in_db=True, reference_amp=self.reference_amplitude)
        filtered = list(filter(lambda peak: peak[1] in self.center_frequencies, peaks))
        filtered.sort(key=lambda peak: peak[1])
        coefficients = []
        i = 0
        # TODO: examine why the plot bounces back and forth; probably something is wrong with how the coeff is evaluated
        for peak in filtered:
            coefficient = -peak[0] + self.target_level
            if coefficient > max_step:
                coefficient = max_step
            if coefficient < -max_step:
                coefficient = -max_step
            if hasattr(self, "coefficients"):
                coefficient += old_coefficients[i][1]
            coefficients.append(coefficient)
            i += 1
        self.coefficients = list(zip([peak[1] for peak in filtered], coefficients))
        self.coefficients.sort(reverse=False)

    # Starting point for learning what the system response is.
    # Stores the result, so that it is possible to equalize incoming data.
    def learn(self, iteration=1):
        i = 0
        while i < iteration:
            self.__evaluate_frequency_response__()
            # self.plot_frequency_response()
            # afc.interpolate_fft(self.frequency_response, self.center_frequencies)
            self.__evaluate_eq_coefficients__()
            i += 1
        print('Learning accomplished')

    def plot_frequency_response_interpolation(self):
        import utils_plt
        x, y = self.frequency_response.get_usable_range(in_db=True, reference_amp=self.reference_amplitude)
        f_peaks = []
        y_peaks = []
        for frequency in self.center_frequencies:
            j = int(round(frequency, 0) - 1)
            f_peaks.append(j + 1)
            y_peaks.append(y[j])
        import numpy as np
        from scipy.interpolate import interp1d
        # temporary solution for low and high
        low = self.center_frequencies[0]
        high = self.center_frequencies[-1]
        x_new = np.arange(low, high + 1, 1)
        interpolation_f = interp1d(f_peaks, y_peaks, 'cubic')  # CubicSpline(f_peaks, y_peaks)
        y_new = interpolation_f(x_new)
        utils_plt.adhoc_plot_frequency_domain_signal(x_new, y_new, "1D-cubic interpolation, only peaks")

    def plot_frequency_response(self):
        import utils_plt
        x, y = self.frequency_response.get_usable_range(in_db=True, reference_amp=self.reference_amplitude)
        utils_plt.adhoc_plot_frequency_domain_signal(x, y)

    # Trained eq ready for usage.
    # Returns equalized data.
    def eq(self, data, apply_only_bandpass=False):
        if not hasattr(self, "coefficients"):
            print("No learning has been performed!")
            return data
        equalized = None
        i = 1
        for coefficient in self.coefficients:
            frequency = coefficient[0]
            gain = coefficient[1]
            if i == 1 and apply_only_bandpass is False:
                filtered = Filter.apply_gain(gain=gain,
                                             data=Filter.low_pass(data=data,
                                                                  cutoff=frequency*(2**(self.bandwidth/2)),
                                                                  fs=SAMPLE_RATE,
                                                                  order=6))
            elif i == len(self.coefficients) and apply_only_bandpass is False:
                filtered = Filter.apply_gain(gain=gain,
                                             data=Filter.high_pass(data=data,
                                                                   cutoff=frequency/(2**(self.bandwidth/2)),
                                                                   fs=SAMPLE_RATE,
                                                                   order=6))
            else:
                filtered = Filter.apply_gain(gain=gain,
                                             data=Filter.band_pass(data=data,
                                                                   fc=frequency,
                                                                   bandwidth=self.bandwidth,
                                                                   fs=SAMPLE_RATE,
                                                                   order=6))
            if equalized is None:
                equalized = filtered
            else:
                equalized += filtered
            i += 1
        return equalized
