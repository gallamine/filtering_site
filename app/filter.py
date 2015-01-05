import numpy as np
import io
from flask import send_file
from flask import jsonify
from scipy import signal
import json

class Filter():

    fir_coeff = []
    config = {}
    data = []
    fid = 0

    supported_types = ['lpf', 'hpf']

    def __init__(self,fid):
        self.fid = fid

    def makeFilter(self,filt_type, config):
        if filt_type in self.supported_types:
            self.config = config
            if filt_type == "lpf":
                return self._makeFIR(config['num_taps'], config['cutoff'], config['window'], config['pass_zero'])

            elif filt_type == "hpf":
                return jsonify({"error": "try 'pass_zero=False'"})
        else:
            return jsonify({'error': 'Unsupported filter {0}'.format(filt_type)})

    def _makeFIR(self, num_taps=40, cutoff=0.5, window=('kaiser', 8), pass_zero=True):
        """
        Get taps for a FIR filter (via windowing method)
        http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.firwin.html
        :type num_taps: int
        :type cutoff: float or list of floats
        :type window: tuple or string
        :type pass_zero: boolean
        :return:
        """
        assert type(pass_zero) is bool

        try:
            self.fir_coeff = signal.firwin(int(num_taps), float(cutoff), window=window, pass_zero=pass_zero)
            self.data = np.zeros(int(num_taps))
            return True
        except Exception as e:
            # Return the numpy error. This is safe (??)
            return jsonify({"error": e.message})

    def runFilter(self, new_data, padding=True):
        '''

        :param new_data: New data to be filtered
        :return: the filtered data of the same length as the input data
        '''
        new_data = new_data.strip('[]')
        new_data = [float(i) for i in new_data.split(',') if i is not '']
        try:
            if len(new_data) > len(self.fir_coeff):
                if padding is True:
                    #TODO: The two lines below need to be tested
                    new_data = np.concatenate((self.data, new_data))  # Filter history
                    self.data = new_data[-len(self.fir_coeff):] #Only save the last bit of data to give filter history

                filtered_signal = signal.lfilter(self.fir_coeff, 1.0, new_data)
                return filtered_signal
                #return filtered_signal[len(self.fir_coeff):]
            else:
                self.data = np.roll(self.data, -len(new_data))  #Shift old data out
                self.data[-len(new_data):] = new_data     #Shift in new data
                filtered_signal = signal.lfilter(self.fir_coeff, 1.0, self.data)
                return filtered_signal[-len(new_data):]
        except Exception as e:
            print e
            return {'error':'??'}

    def returnTaps(self):
        '''

        :return: taps in json format
        '''
        return self.fir_coeff.tolist()


    def returnTapPlot(self):
        '''

        :return: A matplotlib image of the filter taps
        '''

        import matplotlib.pyplot as plt

        fig = plt.figure()
        plt.title('{0} Filter taps'.format(self.fid))
        plt.stem(self.fir_coeff)
        plt.axis('tight')
        buf = io.BytesIO()
        plt.savefig(buf,format= 'png')
        buf.seek(0)
        return send_file(buf,\
                     attachment_filename='taps.png',\
                     mimetype='image/png')

    def returnSpectrum(self):
        '''

        :return: A matplotlib image of the filter spectrum
        '''
        w, h = signal.freqz(self.fir_coeff)

        import matplotlib.pyplot as plt
        fig = plt.figure()
        plt.title('Digital filter frequency response')
        ax1 = fig.add_subplot(111)

        plt.plot(w, 20 * np.log10(abs(h)), 'b')
        plt.ylabel('Amplitude [dB]', color='b')
        plt.xlabel('Frequency [rad/sample]')

        ax2 = ax1.twinx()
        angles = np.unwrap(np.angle(h))
        plt.plot(w, angles, 'g')
        plt.ylabel('Angle (radians)', color='g')
        plt.grid()
        plt.axis('tight')

        buf = io.BytesIO()
        plt.savefig(buf, format = 'png')
        buf.seek(0)
        return send_file(buf,\
                     attachment_filename='spectrum.png',\
                     mimetype='image/png')

