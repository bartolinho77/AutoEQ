import numpy as np
import copy as cp


def sum_ffts(ffts):
    initialize = True
    for fft in ffts:
        if initialize:
            summary_fft = cp.deepcopy(fft)
            initialize = False
        summary_fft.f_abs += fft.f_abs
        summary_fft.psd += fft.psd
    return summary_fft


def sum_signals(sigs):
    from Signal import Signal
    summary_sig = Signal(d=sigs[0].d)
    summary_sig.prepare_x_axis()
    for sig in sigs:
        if summary_sig.y is None:
            summary_sig.y = sig.y
            continue
        summary_sig.y += sig.y
    return summary_sig


def get_frequency_distribution(low=200, high=5000, steps=10):
    import math as m
    return np.floor(np.logspace(m.log10(low), m.log10(high), steps))


def voss(nrows, ncols=16):
    import pandas as pd
    """Generates pink noise using the Voss-McCartney algorithm.

    nrows: number of values to generate
    rcols: number of random sources to add

    returns: NumPy array
    """
    array = np.empty((nrows, ncols))
    array.fill(np.nan)
    array[0, :] = np.random.random(ncols)
    array[:, 0] = np.random.random(nrows)

    # the total number of changes is nrows
    n = nrows
    cols = np.random.geometric(0.5, n)
    cols[cols >= ncols] = 0
    rows = np.random.randint(nrows, size=n)
    array[rows, cols] = np.random.random(n)

    df = pd.DataFrame(array)
    df.fillna(method='ffill', axis=0, inplace=True)
    total = df.sum(axis=1)

    return total.values
