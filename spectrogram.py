import matplotlib
import matplotlib.pyplot as plt, mpld3
matplotlib.use('agg',warn=False, force=True)
from matplotlib import pyplot as plt
print "Switched to:",matplotlib.get_backend()
import numpy as np

a0 = 308.3544123
b1 = 2.694788256
b2 = -0.001241211577
b3 = -0.000006200191144
b4 = 0.000000002366853875
b5 = 0.00000000001565177015


def get_poly(pix):
    return (a0 + b1 * pix + b2 * (pix ** 2) + b3 * (pix ** 3) + b4 * (pix ** 4) + b5 * (pix ** 5))


wavelengths_x = [get_poly(i + 1) for i in range(288)]


def get_average_spectrogram(input_spectra):
    np_array = np.array(input_spectra)
    return np.mean(np_array, axis=0)


def generate_raw_spectrogram(input_array):
    out_plot = plt.plot(wavelengths_x, input_array)
    plt.ylabel('Intensity')
    plt.xlabel('Wavelength')

    return out_plot


def generate_relative_spectrogram(input_array):
    max_value = np.max(input_array)
    max_arg = np.argmax(input_array)

    scaled_inputs = [(i / max_value) for i in input_array]

    out_plot = plt.plot(wavelengths_x, scaled_inputs)
    plt.ylabel('Relative Intensity %')
    plt.xlabel('Wavelength')

    plt.annotate("Peak Wavelength: {}nm".format(round(wavelengths_x[max_arg], 1)), xy=(0.3, 0.05),
                 xycoords='axes fraction', fontsize=10)

    return out_plot

def generate_html_spectrogram(intput_array):
    fig = plt.figure()
    generate_relative_spectrogram(intput_array)

    return(mpld3.fig_to_html(fig))