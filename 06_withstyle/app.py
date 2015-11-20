from flask import Flask, render_template

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

if __name__ == '__main__':
    app.run(debug=True)
