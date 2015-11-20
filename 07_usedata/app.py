from flask import Flask, render_template

class Dummy(object):
    """ Dummy object with dummy properties. """

    def __init__(self, name, present=False):
        self.name = name
        self.present = present

# Create app
app = Flask(__name__)

# Default route
@app.route('/')
def index():
    return 'Hello World!'

# Echo
@app.route('/echo/<word>')
def echo(word):
    return 'You said: %s' % word

# Superecho
@app.route('/superecho/<word>')
def superecho(word):
    return render_template('superecho.html', word=word)

# Using data
@app.route('/data')
def data():
    dummy_a = Dummy('Person A')
    dummy_b = Dummy('Person B', True)

    data_list = [3, 14, 9, 58, 'potato', 12, 38, 37.19, 'nyan']
    people = [dummy_a, dummy_b]

    return render_template('showdata.html', data=data_list, people=people)

if __name__ == '__main__':
    app.run(debug=True)
