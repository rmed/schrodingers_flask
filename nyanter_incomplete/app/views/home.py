from flask import Blueprint, render_template, request, url_for, \
        redirect, session, flash
from playhouse.flask_utils import get_object_or_404, object_list
from peewee import IntegrityError

from ..models import User
from ._util import login_required

home = Blueprint('home', __name__)

#TODO
@home.route()
def index():
    """ Show dummy index. """
    if session.get('logged_in', False):
        #TODO
        # Redirect to profile
        return 

    #TODO
    return

#TODO
@home.route()
def login():
    """ Perform login. """
    if session.get('logged_in', False):
        #TODO
        # Redirect to profile
        return 

        # Perform login
        #TODO

        # Check password
        if not user or not user.check_password(request.form['password']):
            # Invalid
            flash('Invalid login information')
            return #TODO 

        # Valid
        session['logged_in'] = True
        session['user'] = user.username

        return #TODO 

    return #TODO 

#TODO
@home.route()
@login_required
def logout():
    """ Perform logout. """
    # Remove info from session
    session.pop('user', None)
    session.pop('logged_in', None)

    return #TODO

#TODO
@home.route()
def signup():
    """ Create a new user account. """
    if session.get('logged_in', False):
        #TODO
        # Redirect to profile
        return 

        # Create new user
        try:
            #TODO
            user = 

            flash('Success, you can now proceed to login')

        except IntegrityError:
            flash('Username or email are already taken')

    return #TODO 
