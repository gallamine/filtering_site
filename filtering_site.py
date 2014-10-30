from flask import Flask
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
    return 'Hello World!'

@app.route('/spectrum/')
def show_spectrum():
    f = filter.Filter()
    f.make_FIR_LPF()
    return f.return_spectrum()

if __name__ == '__main__':
    app.run(debug=True)
