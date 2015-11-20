from flask import Flask

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

# dot what?
@app.route('/myapp.java')
def wut():
    return 'No java for you!'

if __name__ == '__main__':
    app.run()
