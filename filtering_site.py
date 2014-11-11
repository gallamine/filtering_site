from flask import Flask
from flask import request
from flask.ext import restful
import filter
import uuid
import json
import db

app = Flask(__name__)
api = restful.Api(app)

all_filters = {}

class FilterHandle(restful.Resource):
    def createNewFilter(self):
        fid = uuid.uuid4()
        try:
            all_filters[str(fid)] = filter.Filter(fid)

            filt_type = request.args.get('type','lpf')
            num_taps = request.args.get('num_taps',40)
            cutoff = request.args.get('cutoff',0.5)
            # TODO: What other windows does scipy support?
            window=('kaiser',8)
            config = {'num_taps':num_taps,'cutoff':cutoff,'window':window}
            all_filters[str(fid)].makeFilter(filt_type,config)
            # Save to disk the list of filters
            db.writeKey('all_filters',all_filters)
            return {'fid':str(fid)}
        except Exception as e:
            return {'error':e}


    def get(self,command):
        '''

        :type fid: unicode
        :type command: unicode
        :return:
        '''
        if command == "new":
            # Create a new filter object
            return self.createNewFilter()

        else:
            fid = request.args.get('fid','')
            if fid in all_filters.keys():

                if command == "taps":
                    return {'taps':all_filters[fid].returnTaps()}
                elif command == "run":
                    # Run the filter using the data provided in data
                    data = request.args.get('data','')

                    if data == '':
                        return {'error':'Send me some data!'}
                    else:
                        data_resp = all_filters[fid].runFilter(data)
                        # TODO: Save only the upated one
                        if isinstance(data_resp, dict):
                            return data_resp
                        else:
                            db.writeKey('all_filters',all_filters)
                            return {'fid':fid,'data_in':data,'data_out':data_resp.tolist()}
                else:
                    return {'hello': 'world','fid':fid}
            else:
                return {'error':"Invalid filter ID"}

api.add_resource(FilterHandle, '/filter/<command>')

class FilterPlotting(restful.Resource):
    def get(self,fid,command):
        '''

        :type fid: unicode Filter ID. You get this by callling filter/new
        :type command: unicode Plot commands (spectrum and taps
        :return: whatever is supposed to come out
        '''
        if fid in all_filters.keys():
            if command == "spectrum":
                # Plot the filter spectrum
                # TODO: Accept sample rate to scale the plot
                return all_filters[fid].returnSpectrum()

            elif command == "taps":
                 # Plot the filter taps
                return all_filters[fid].returnTapPlot()

        else:
            return {'error':"Invalid filter ID"}

api.add_resource(FilterPlotting, '/filter/<fid>/plots/<command>')

@app.route('/')
def hello_world():
    #args_dict = request.args
    #return args_dict
    return 'Go to /filter/new to get a filter handle!<br>'

@app.route('/spectrum/<filt_type>')
def show_spectrum(filt_type):
    f = filter.Filter()
    try:
        num_taps = request.args.get('num_taps','')
        cutoff = request.args.get('cutoff','')
    except:
        num_taps = 40
        cutoff = 0.5
    window=('kaiser',8)
    f.make_FIR_LPF(num_taps,cutoff,window)
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
    # Load filters from db
    try:
        all_filters = db.readKey('all_filters')
        if all_filters is False:
            all_filters = {}
    except:
        print "No filters saved"


    app.run(passthrough_errors = True)
    #app.run(debug=True)
