from flask import Flask, render_template
from playhouse.flask_utils import FlaskDB

from .models import db_proxy, User, Nya, Subscription

from .views.home import home
from .views.board import board
from .views.fserver import fserver
from .views.profile import profile

import os

# Create app
app = Flask(__name__, instance_relative_config=True)


# Load configuration specified in env var or default development one
# Production configurations from /instance
cfg = os.getenv('PRODUCTION_CONFIG', None)
if cfg:
    app.config.from_envvar('PRODUCTION_CONFIG')
else:
    app.config.from_object('config.development')


# Setup database
flask_db = FlaskDB(app)
db_proxy.initialize(flask_db.database)

# Create tables
flask_db.database.create_tables([User, Nya, Subscription], safe=True)


# Blueprints
app.register_blueprint(home)
app.register_blueprint(board)
app.register_blueprint(fserver, url_prefix='/media')
app.register_blueprint(profile, url_prefix='/nyan')

# 404 handler
@app.errorhandler(404)
def not_found(e):
    msg = 'Nothing to see here, move along!'
    return render_template('error.html', error_code=404, error_msg=msg)

# 403 handler
@app.errorhandler(403)
def not_found(e):
    msg = "You tried to do something forbidden, didn't you?"
    return render_template('error.html', error_code=403, error_msg=msg)
