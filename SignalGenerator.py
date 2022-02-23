from Signal import *


class SignalGenerator:
    # returns a Signal object; windowing is applied
    @staticmethod
    def sine(duration=1, amplitude=1, frequency=1000, zero_tail=False):
        sine = Signal(f=frequency, d=duration)
        sine.y = amplitude * np.sin(2 * np.pi * frequency * sine.t)
        sine.y = sine.y.squeeze()
        if zero_tail:
            n = len(sine.y)
            m = int(0.9 * n)
            p = np.argmin(np.abs(sine.y[m:]))
            r = m + p
            while r < n:
                sine.y[r] = 0
                r += 1
        return sine

    @staticmethod
    def chirp(duration=1, amplitude=1, start_frequency=20, end_frequency=20000):
        from scipy.signal import chirp
        model_signal = Signal(d=duration)
        model_signal.y = amplitude * chirp(t=model_signal.t,
                                           f0=start_frequency, f1=end_frequency,
                                           t1=model_signal.t[len(model_signal.t) - 1],
                                           method='logarithmic', phi=90)
        return model_signal
