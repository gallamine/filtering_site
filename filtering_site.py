import db as dbclass
from flask import Flask
from flask import request
from flask.ext import restful
from flask import jsonify
import filter
import uuid
import json


class MyServer(Flask):

    def __init__(self, *args, **kwargs):
        super(MyServer, self).__init__(*args, **kwargs)

        try:
            APPLICATION_PATH = "/Users/william/Documents/filtering_site/"
            f = open(APPLICATION_PATH + '.mongo', 'r')
            username, password = f.read().split("\t")
            # Load filters from db
            self.db = dbclass.Database(username, password)

            self.all_filters = self.db.loadAllFilters() #db.readKey('all_filters')
            if self.all_filters is False:
                self.all_filters = {}

        except:
            print "No filters saved"

app = MyServer(__name__)
api = restful.Api(app)


def createNewFilter(request):
    """

    :return:
    """

    fid = uuid.uuid4()
    try:
        app.all_filters[str(fid)] = filter.Filter(fid)

        filt_type = request.args.get('type','lpf')
        #TODO: Put an upper limit on the tap size
        num_taps = request.args.get('num_taps', 40)
        cutoff = request.args.get('cutoff',0.5)
        # TODO: What other windows does scipy support?
        window = ('kaiser', 8)
        config = {'num_taps': num_taps, 'cutoff': cutoff, 'window': window}
        app.all_filters[str(fid)].makeFilter(filt_type, config)

        app.db.saveFilter(app.all_filters[str(fid)])
        return jsonify({'fid': str(fid)})
    except Exception as e:
        #TODO: This is a big security no-no
        return jsonify({'error': e})


@app.route('/filter/<command>')
def filter_commands(command):
    """
    Operations to do to a filter pass the FID via fid=XXXXX arguemnt
    :param command:
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
                        data_resp = app.all_filters[fid].runFilter(data)
                        if isinstance(data_resp, dict):
                            return jsonify(data_resp)
                        else:
                            app.db.saveFilter(app.all_filters[fid])
                            return jsonify({'fid': fid, 'data_in': data, 'data_out': data_resp.tolist()})
                else:
                    return jsonify({'hello': 'world', 'fid': fid})
            else:
                return jsonify({'error': "Invalid filter ID"})


@app.route('/filter/<fid>/plots/<command>')
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
    return 'Go to /filter/new to get a filter handle!<br>'

@app.route('/spectrum/<filt_type>')
def show_spectrum(filt_type):
    """
    Draw a spectrum for the specififed filter type. Don't save the filter
    :param filt_type:
    :return:
    """
    f = filter.Filter()
    try:
        num_taps = request.args.get('num_taps','')
        cutoff = request.args.get('cutoff','')
    except:
        num_taps = 40
        cutoff = 0.5
    window = ('kaiser',8)
    f.make_FIR_LPF(num_taps, cutoff, window)
    return f.returnSpectrum()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

if __name__ == '__main__':

    app.run(passthrough_errors = True)
    #app.run(debug=True)
