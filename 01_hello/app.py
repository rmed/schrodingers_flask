from flask import Flask

# Create app
app = Flask(__name__)

# Default route
@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
