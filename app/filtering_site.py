import uuid
from app import app
from flask import Flask
from flask import request
from flask.ext import restful
from flask import jsonify
import dsp_helpers
from app import db as dbclass
import filter
from flask.ext.cors import CORS, cross_origin

MAX_TAPS = 8192


def createNewFilter(request):
    """
    Create a new filter based on the input parameters
    :return:
    """

    fid = uuid.uuid4()
    try:
        app.all_filters[str(fid)] = filter.Filter(fid)
        # TODO: Automatically expand the list of parameters so the scipy docs can be followed exactly
        filt_type = request.args.get('type', 'lpf')
        num_taps = request.args.get('num_taps', 40)
        if num_taps > MAX_TAPS:
            num_taps = MAX_TAPS
            #TODO: Return an warning that the output was coerced.

        cutoff = request.args.get('cutoff', 0.5)
        window = request.args.get('window', 'hamming')   # Another example "('kaiser',8)"
        pass_zero = request.args.get('pass_zero', "True")  # Default is LPF
        if pass_zero == "false" or pass_zero == "False":
            pass_zero = False
        else:
            pass_zero = True

        config = {'num_taps': num_taps, 'cutoff': cutoff, 'window': window, 'pass_zero': pass_zero}
        ret = app.all_filters[str(fid)].makeFilter(filt_type, config)
        if ret is not True:
            return ret


        app.db.saveFilter(app.all_filters[str(fid)])
        return jsonify({'fid': str(fid)})
    except Exception as e:
        #TODO: This is a big security no-no
        return jsonify({'error': e})


@app.route('/fft/')
@cross_origin()
def fft_commands():
    """
    Return fourier constants
    :return:
    """

    if request.args is None:
        return "Pass in data via ?data=[1,2,3, ... ]. Fs is specified via ?fs=samples_per_timeperiod"

    data = request.args.get('data')
    if data is None:
        return "Send data"
    try:
        fs = request.args.get('fs', 1.0)
        window = request.args.get('window', None)

        dsp_helper.fft(data)
    except:
        fs = None
        window = ('kaiser',8)



    return False


@app.route('/filter/get_windows')
@cross_origin()
def get_windows():
    """
    Return a list of all the FIR windows you can use
    http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.get_window.html#scipy.signal.get_window
    :return:
    """
    # TODO: How to support tuples in the request string?
    window_type = request.args.get('type')
    if window_type is None:
        return jsonify(dsp_helpers.get_window("all"))

    else:
        nx = request.args.get('nx', 100)
        return jsonify(dsp_helpers.get_window(window_type))

    #TODO: Implement this function to return a list of all windows

    return False


@app.route('/filter/<command>')
@cross_origin()
def filter_commands(command):
    """
    Operations to do to a filter pass the FID via fid=XXXXX argument
    padding=True preserves filter history (data isn't 0 at beginning, it's the remainder of the old data
    window = string or tuple of string and parameter values
    :param command: new, taps, run
    :return:
    """

    if request.method == 'GET':

        if command == "new":
            # Create a new filter object
            return createNewFilter(request)

        else:
            fid = request.args.get('fid', '')
            if fid in app.all_filters.keys():

                if command == "taps":
                    return jsonify({'taps': app.all_filters[fid].returnTaps()})

                elif command == "run":
                    # Run the filter using the data provided in data
                    data = request.args.get('data', '')

                    if data == '':
                        return jsonify({'error': 'Send me some data!'})
                    else:
                        padding = request.args.get('padding', 'True')    # Preserve filter history
                        if padding == "false" or padding == "False":
                            padding = False
                        else:
                            padding = True
                        data_resp = app.all_filters[fid].runFilter(data, padding)
                        if isinstance(data_resp, dict):
                            return jsonify(data_resp)
                        else:
                            app.db.saveFilter(app.all_filters[fid])
                            return jsonify({'fid': fid,
                                            'data_in': data,
                                            'data_out': data_resp.tolist(),
                                            'padding': padding})
                else:
                    return jsonify({'hello': 'world', 'fid': fid})
            else:
                return jsonify({'error': "Invalid filter ID"})


@app.route('/filter/<fid>/plots/<command>')
@cross_origin()
def filter_plotting(fid, command):
    '''

    :type fid: unicode Filter ID. You get this by callling filter/new
    :type command: unicode Plot commands (spectrum and taps
    :return: whatever is supposed to come out
    '''
    if request.method == 'GET':
        if fid in app.all_filters.keys():
            if command == "spectrum":
                # Plot the filter spectrum
                # TODO: Accept sample rate to scale the plot
                return app.all_filters[fid].returnSpectrum()

            elif command == "taps":
                 # Plot the filter taps
                return app.all_filters[fid].returnTapPlot()

        else:
            return jsonify({'error': "Invalid filter ID"})

@app.route('/')
def hello_world():
    #args_dict = request.args
    #return args_dict
    doc = """
    /filter/new returns a FID string. Use this to reference your filter. This string is referenced below as <fid>
    <Br>
    /filter/<fid>/plots/taps returns a plot of the filter taps
    <br>
    /filter/<fid>/plots/spectrum returns a plot of the filter spectrum
    <br>
    /filter/taps?fid=<fid> returns a json dictionary of the filter tap values if you'd like to use it in another project.
    <br>
    /filter/run?fid=<fid>&data=[comma,separated,array,of,values] will run the filter using the supplied data. It has memory,
    meaning running it in succession will change the output until it reaches a steady state value. To turn off memory supply
    the &padding=False argument when running.
    When run the filter will return a json dict of the input data and hte output data.

    """
    return 'Go to /filter/new to get a filter handle!<br>'

@app.route('/spectrum/<filt_type>')
@cross_origin()
def show_spectrum(filt_type):
    """
    Draw a spectrum for the specififed filter type. Don't save the filter
    :param filt_type:
    :return:
    """
    f = filter.Filter()
    try:
        num_taps = request.args.get('num_taps', '')
        cutoff = request.args.get('cutoff', '')
    except:
        num_taps = 40
        cutoff = 0.5
    window = ('kaiser', 8)
    f.make_FIR_LPF(num_taps, cutoff, window)
    return f.returnSpectrum()


