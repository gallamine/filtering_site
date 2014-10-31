import numpy as np
import io
from flask import send_file
from scipy import signal

class Filter():

    b = []

    def make_FIR_LPF(self,num_taps=40,cutoff=0.5,window=('kaiser',8)):

        self.b = signal.firwin(int(num_taps), float(cutoff), window=window)
        return True

    def return_spectrum(self):
        w, h = signal.freqz(self.b)

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