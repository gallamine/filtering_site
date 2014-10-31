from flask import Flask
from flask import request
from flask.ext import restful
import filter

app = Flask(__name__)
api = restful.Api(app)

class HelloWorld(restful.Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/api')

@app.route('/')
def hello_world():
    #args_dict = request.args
    #return args_dict
    return 'Hello World!'

@app.route('/spectrum/')
def show_spectrum():
    f = filter.Filter()
    try:
        num_taps = request.args.get('num_taps','')
        cutoff = request.args.get('cutoff','')
    except:
        num_taps = 40
        cutoff = 0.5
    window=('kaiser',8)
    f.make_FIR_LPF(num_taps,cutoff,window)
    return f.return_spectrum()

if __name__ == '__main__':
    app.run(debug=True)
