import numpy as np
import scipy.signal as signal
import scipy.fftpack as fftpack


def get_window(window_type, nx=100):
    """
    Return coeffcients for various windows. If `window_type` is "all" return a list of them all
    :param window_type:
    :return:
    """
    if window_type == "all":
        return {'windows': signal.windows.__all__}

    else:
        try:
            return {'coeff':signal.get_window(str(window_type), nx).tolist()}
        except Exception as e:
            return {'error':e.message}


def compute_fft(x, n=None, axis=True, power=True, fftshift=True, fs=1.0):
    """
    Compute and return the FFT of the input data
    :param x:
    :param n:
    :param power:
    :param fftshift:
    :return:
    """
    x = x.strip('[]')
    x = [float(i) for i in x.split(',') if i is not '']

    fft_out = fftpack.fft(x,n)

    if axis is True:
        axis_values = np.linspace(0, 2*fs, len(fft_out))
    else:
        axis_values = []

    if power is True:
        fft_out = np.abs(fft_out)

    if fftshift is True:
        fft_out = fftpack.fftshift(fft_out)
        axis_values = fftpack.fftshift(axis_values)

    outdict = {'data_in': x,
               'data_out': fft_out,
               'axis':axis_values,
                'power':power,
                'fft_shift':fft_shift}