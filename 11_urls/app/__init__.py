from flask import Flask, render_template, request
from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list
from werkzeug.exceptions import NotFound

from .models import User, db_proxy

# Create app
app = Flask(__name__)
app.config['DATABASE'] = 'sqlite:///devdb.sqlite'

# Setup DB
flask_db = FlaskDB(app)
db_proxy.initialize(flask_db.database)

# Create tables
flask_db.database.create_tables([User], safe=True)

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

# Using forms
@app.route('/superform', methods=['GET', 'POST'])
def superform():
    if request.method == 'POST':
        name = request.form['name']

        User.create(name=name)

    # Fetch all users
    users = User.select()

    try:
        return object_list('superform.html',
                query=users,
                context_variable='users')

    except NotFound:
        # Prevent 404 and show nicer message
        return render_template('superform.html')

# URLs in templates
@app.route('/urls')
def urls():
    return render_template('urls.html')
