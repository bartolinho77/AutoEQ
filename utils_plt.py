import matplotlib.pyplot as plt


def plot_time_signal(signal, label="Generated signal"):
    fig, ax = plt.subplots()
    if signal.f is None:
        title = "Time domain - Summary signal"
    else:
        title = "Time domain - Sine - " + str(signal.f) + " Hz"
    ax.set_title(title)
    ax.set_ylabel("Amplitude")
    ax.set_xlabel("Time (s)")
    ax.grid(b=True, which='both')
    plt.sca(ax)
    plt.plot(signal.t, signal.y, color='b', LineWidth=2, label=label)
    plt.legend()
    plt.show()


def plot_frequency_domain_signal(signal, label="Generated signal"):
    fig, ax = plt.subplots()
    title = "Frequency domain - " + str(signal.n/signal.fs) + " s"
    ax.set_title(title)
    ax.set_ylabel("Amplitude")
    ax.set_xlabel("Frequency (Hz)")
    plt.sca(ax)
    x, y = signal.get_usable_range(in_db=True, reference_amp=0.5)
    plt.plot(x, y, color='k', LineWidth=2, label=label)
    ax.set_xscale('log')
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.grid(b=True, which='both')
    ax.set_xlim([15, 25000])
    plt.legend()
    plt.show()


def adhoc_plot_time_domain_signal(x, y):
    fig, axs = plt.subplots(nrows=1, ncols=1)
    title = "Time domain"
    axs.set_title(title)
    axs.set_ylabel("Amplitude")
    axs.set_xlabel("Time (s)")
    plt.sca(axs)
    plt.plot(x, y, color='c', LineWidth=2, label='Generated signal')
    axs.grid(b=True, which='both')
    plt.legend()
    plt.show()


def adhoc_plot_frequency_domain_signal(x, y, label="Generated signal"):
    fig, ax = plt.subplots()
    title = "Frequency domain"
    ax.set_title(title)
    ax.set_ylabel("Amplitude")
    ax.set_xlabel("Frequency (Hz)")
    plt.sca(ax)
    plt.plot(x, y, color='k', LineWidth=2, label=label)
    ax.set_xscale('log')
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.grid(b=True, which='both')
    ax.set_xlim([15, 25000])
    plt.legend()
    plt.show()


def plot_results(m_s, m_fft, r_s, r_fft):
    fig, axs = plt.subplots(nrows=2, ncols=1)
    title = "Time domain - " + str(m_s.f) + " Hz"
    axs[0].set_title(title)
    title = "Frequency domain - " + str(m_s.d) + " s"
    axs[1].set_title(title)
    axs[0].set_ylabel("Amplitude")
    axs[0].set_xlabel("Time (s)")
    axs[1].set_ylabel("Amplitude")
    axs[1].set_xlabel("Frequency (Hz)")
    plt.sca(axs[0])
    plt.plot(m_s.t, m_s.y, color='c', LineWidth=2, label='Generated signal')
    plt.plot(r_s.t, r_s.y, color='m', LineWidth=1.5, label='Recorded signal')
    plt.legend()
    plt.sca(axs[1])
    m_x, m_y = m_fft.get_usable_range()
    plt.plot(m_x, m_y, color='c', LineWidth=2,
             label='Generated signal frequency spectrum')
    r_x, r_y = r_fft.get_usable_range()
    plt.plot(r_x, r_y, color='m', LineWidth=1.5,
             label='Recorded signal frequency spectrum')

    axs[1].set_xscale('log')
    axs[1].xaxis.set_major_formatter('{x:.0f}')
    # axs[1].xaxis.set_minor_formatter('{x:.0f}')
    # axs[1].tick_params(which='major', length=13)
    # axs[1].tick_params(which='minor', length=4)
    axs[0].grid(b=True, which='both')
    axs[1].grid(b=True, which='both')
    axs[1].set_xlim([15, 25000])
    plt.legend()
    plt.show()
