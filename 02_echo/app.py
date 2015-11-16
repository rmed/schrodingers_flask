from flask import Flask

# Create app
app = Flask(__name__)

# Default route
@app.route('/')
def index():
    return 'Hello World!'

# Echo
@app.route('/<name>')
def echo(name):
    return 'Hello %s!' % name

if __name__ == '__main__':
    app.run()
