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
    return center_sp, frequency_readings(n)


def frequency_readings(n):
    f_readings = fft.fftfreq(n, 1 / n)
    return fft.fftshift(f_readings)


def signal_quantization(sign, F_filter, Fs):
    params = calculation_of_filter_parameters(F_filter, Fs)
    quantized_signals = []
    dispersions = []
    signals_noise = []

    for M in [4, 16, 64, 256]:
        bits = []
        delta = (numpy.max(sign) - numpy.min(sign)) / (M - 1)
        quantize_signal = delta * numpy.round(sign / delta)
        quantized_signals += [list(quantize_signal)]
        quantize_levels = numpy.arange(numpy.min(quantize_signal), numpy.max(quantize_signal)+1, delta)
        quantize_bit = numpy.arange(0, M)
        quantize_bit = [format(bits, '0' + str(int(numpy.log(M) / numpy.log(2))) + 'b') for bits in quantize_bit]
        quantize_table = numpy.c_[quantize_levels[:M], quantize_bit[:M]]
        bits_table(M, quantize_table, f"Таблиця квантування для {M} рівнів")
        for signal_value in quantize_signal:
            for index, value in enumerate(quantize_levels[:M]):
                if numpy.round(numpy.abs(signal_value - value), 0) == 0:
                    bits.append(quantize_bit[index])
                    break
        bits = [int(item) for item in list(''.join(bits))]
        displaying_the_bits(numpy.arange(0, len(bits)), bits, "Біти", "Амплітуда сигналу",
                            f"кодова послідовність сигналу при кількості рівнів квантування {M}",
                            grid=True)
        qwe = signal.sosfiltfilt(params, quantize_signal)
        e1 = qwe - sign
        dispersion = numpy.var(e1)
        dispersions += [dispersion]
        signals_noise += [numpy.var(sign) / dispersion]
    return dispersions, signals_noise, quantized_signals


def bits_table(m, quantize_table, name):
    fig, ax = plt.subplots(figsize=(14 / 2.54, m / 2.54))
    table = ax.table(cellText=quantize_table, colLabels=['Значення сигналу', 'Кодова послідовність'], loc='center')
    table.set_fontsize(14)
    table.scale(1, 2)
    ax.axis('off')
    fig.savefig(f"./figures/{name}.png", dpi=600)


def displaying_the_results(x, y, ox_txt, oy_txt, name, grid=False):
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.plot(x, y, linewidth=1)
    ax.set_xlabel(ox_txt, fontsize=14)
    ax.set_ylabel(oy_txt, fontsize=14)
    plt.title(name, fontsize=14)
    if grid:
        plt.grid()
    fig.savefig(f"./figures/{name}.png", dpi=600)


def displaying_the_bits(x, y, ox_txt, oy_txt, name, grid=False):
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.step(x, y, linewidth=0.1)
    ax.set_xlabel(ox_txt, fontsize=14)
    ax.set_ylabel(oy_txt, fontsize=14)
    plt.title(name, fontsize=14)
    if grid:
        plt.grid()
    fig.savefig(f"./figures/{name}.png", dpi=600)


def displaying_the_results_2(x, y, ox_txt, oy_txt, name):
    fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
    s = 0
    for i in range(0, 2):
        for j in range(0, 2):
            ax[i][j].plot(x, y[s], linewidth=1)
            s += 1
    fig.supxlabel(ox_txt, fontsize=14)
    fig.supylabel(oy_txt, fontsize=14)
    fig.suptitle(name, fontsize=14)
    fig.savefig(f"./figures/{name}.png", dpi=600)


def main():
    n = 500
    Fs = 1000
    F_max = 11
    F_filter = 18

    sign = signal_generation(0, 10, n)
    time_counts = determination_of_time_counts(n, Fs)
    filter_params = calculation_of_filter_parameters(F_max, Fs)
    f_sign = signal_filtering(filter_params, sign)
    dispersion, signals_noise, quantized_signals = signal_quantization(f_sign, F_filter, Fs)

    displaying_the_results_2(
        time_counts, quantized_signals, "Час (секунди)", "Амплітуда сигналу",
        "Цифрові сигнали з рівнями квантування (4, 16, 64, 256)")
    displaying_the_results([4, 16, 64, 256], dispersion, "Кількість рівнів квантування",
                           "Дисперсія", "Залежність дисперсії від кількості рівнів квантування", grid=True)
    displaying_the_results([4, 16, 64, 256], signals_noise, "Кількість рівнів квантування",
                           "ССШ", "Залежність співвідношення сигнал-шум від кількості рівнів квантування", grid=True)


if __name__ == "__main__":
    main()
