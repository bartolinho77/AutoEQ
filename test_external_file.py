import numpy as np
from pathlib import Path
from Signal import Signal
from scipy.io.wavfile import read
FILE_PATH = "C:/Users/Bartosz Ireneusz/Desktop/rec.npy"


def load_data_from_file(filepath):
    file = Path(filepath)
    return np.load(file)


def load_wave(filepath, reference_amplitude=0.01):
    a = read(Path(filepath))
    max_value = np.amax(np.abs(a[1]))
    y = np.array(a[1], dtype=float)
    y /= max_value/reference_amplitude
    fs = a[0]
    return y, fs


def save_data_to_file(filepath, array):
    file = Path(filepath)
    np.save(file, array)


def test_for_prerecorded_data():
    model_signal = Signal(f=440, d=10)
    model_signal.generate_sine()
    model_fft = model_signal.get_frequency_representation()

    recorded_signal = Signal(y=load_data_from_file(FILE_PATH), f=440, d=10)
    recorded_fft = recorded_signal.get_frequency_representation()

    # plot_results(model_signal, model_fft, recorded_signal, recorded_fft)
