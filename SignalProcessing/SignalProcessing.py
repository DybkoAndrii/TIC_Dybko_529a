import numpy.random
from scipy import signal, fft
import matplotlib.pyplot as plt


def signal_generation(a, b, n):
    return numpy.random.normal(a, b, n)


def determination_of_time_counts(n, Fs):
    return numpy.arange(n) / Fs


def calculation_of_filter_parameters(F_max, Fs):
    w = F_max / (Fs / 2)
    return signal.butter(3, w, 'low', output='sos')


def signal_filtering(parameters_filter, sign):
    return signal.sosfiltfilt(parameters_filter, sign)


def calculation_of_the_signal_spectrum(f_sign, n):
    spectrum = fft.fft(f_sign)
    center_sp = numpy.abs(fft.fftshift(spectrum))
    f_readings = fft.fftfreq(n, 1/n)
    return center_sp, fft.fftshift(f_readings)


def displaying_the_results(x, y, ox_txt, oy_txt, name):
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.plot(x, y, linewidth=1)
    ax.set_xlabel(ox_txt, fontsize=14)
    ax.set_ylabel(oy_txt, fontsize=14)
    plt.title(name, fontsize=14)
    fig.savefig(f"./figures/{name}.png", dpi=600)


def main():
    n = 500
    Fs = 1000
    F_max = 11

    sign = signal_generation(0, 10, n)
    time_counts = determination_of_time_counts(n, Fs)
    filter_params = calculation_of_filter_parameters(F_max, Fs)
    f_sign = signal_filtering(filter_params, sign)

    displaying_the_results(
        time_counts, f_sign, "Час (с)", "Амплітуда сигналу", "Сигнал с максимальною частотою 11 Гц")

    y, x = calculation_of_the_signal_spectrum(f_sign, n)

    displaying_the_results(x, y, "Частота (Гц)", "Амплітуда спектру", "Спектр сигналу з максимальною частотою 11 Гц")


if __name__ == "__main__":
    main()
