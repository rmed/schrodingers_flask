from flask import Blueprint, render_template, request, url_for, \
        redirect, session, flash
from playhouse.flask_utils import get_object_or_404, object_list
from peewee import IntegrityError

from ..models import User
from ._util import login_required

home = Blueprint('home', __name__)

@home.route('/')
def index():
    """ Show dummy index. """
    if session.get('logged_in', False):
        return redirect(url_for('profile.show'))

    return render_template('home/index.html')

@home.route('/login', methods=['GET', 'POST'])
def login():
    """ Perform login. """
    if session.get('logged_in', False):
        return redirect(url_for('profile.show'))

    if request.method == 'POST':
        # Perform login
        try:
            user = User.get(User.username == request.form['username'])

        except User.DoesNotExist:
            user = None

        # Check password
        if not user or not user.check_password(request.form['password']):
            # Invalid
            flash('Invalid login information')
            return render_template('home/login.html')

        # Valid
        session['logged_in'] = True
        session['user'] = user.username

        return redirect(url_for('profile.show', username=user.username))

    return render_template('home/login.html')

@home.route('/logout')
@login_required
def logout():
    """ Perform logout. """
    # Remove info from session
    session.pop('user', None)
    session.pop('logged_in', None)

    return redirect(url_for('home.index'))

@home.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Create a new user account. """
    if session.get('logged_in', False):
        return redirect(url_for('profile.show'))

    if request.method == 'POST':
        # Create new user
        try:
            user = User.create(
                    username=request.form['username'],
                    email=request.form['email'],
                    password=User.generate_password(request.form['password']))

            flash('Success, you can now proceed to login')

        except IntegrityError:
            flash('Username or email are already taken')

    return render_template('home/signup.html')
