from flask import Blueprint, render_template, request, \
        url_for, redirect, session, flash, abort, current_app
from peewee import IntegrityError
from playhouse.flask_utils import get_object_or_404, object_list
from werkzeug import secure_filename
from werkzeug.exceptions import NotFound

from ..models import User, Nya, Subscription
from ._util import login_required, forbid_owner

import os

profile = Blueprint('profile', __name__)

@profile.route('/', defaults={'username': None})
#TODO
@profile.route()
@login_required
def show(username):
    """ Show a profile. """
    if not username:
        username = session.get('user', None)

    # Get user and self
    try:
        #TODO

    except User.DoesNotExist:
        abort(404)

    # Check if following
    try:
        #TODO
        sub = 

        # Exists
        is_following = True

    except Subscription.DoesNotExist:
        is_following = False

    # Get nyas
    if myself.username == username:
        # My account, show own and subscriptions
        nyas = (Nya
                .select(Nya, User)
                .join(User)
                .where(
                    (Nya.author == user) |
                    (Nya.author << user.subscriptions))
                .order_by(Nya.timestamp.desc())
                )

    else:
        # Another user's account
        nyas = (Nya
                .select(Nya, User)
                .join(User)
                .where(Nya.author == user)
                .order_by(Nya.timestamp.desc())
                )

    try:
        #TODO
        #object_list

    except NotFound:
        # Prevent 404 and show nicer message
        return render_template('profile/show.html', user=user)

#TODO
@profile.route()
@login_required
def new_nya():
    """ Publish a new Nya. """
    if request.method == 'POST':
        username = session.get('user', None)

        # Get user
        #TODO

        #TODO
        message = 

        # Create Nya
        #TODO
        nya = 

        # TODO
        # Redirect to profile

    # Show form
    return render_template('profile/new_nya.html')

@profile.route('/toggle-follow', defaults={'username': None})
#TODO
@profile.route()
@login_required
@forbid_owner
def toggle_follow(username):
    """ (Un)Subscribe to another user. """
    # Get user and self
    try:
        # TODO

    except User.DoesNotExist:
        # Oops
        abort(404)

    # Check if following
    try:
        #TODO
        sub = 

        # Exists
        is_following = True

    except Subscription.DoesNotExist:
        is_following = False


    if is_following:
        # Unfollow
        #TODO

    else:
        # Follow
        #TODO

    # Show profile
    #TODO

#TODO
@profile.route()
@login_required
def edit():
    """ Edit user information. """
    # Get user
    username = session.get('user', None)
    try:
        user = User.get(User.username == username)

    except User.DoesNotExist:
        abort(404)

    if request.method == 'POST':
        #TODO
        # Edit information

        # Update user information
        try:
            user.save()

            flash('Success, changes saved')
            session['user'] = request.form['username']

            # Change profile pic
            pic = request.files['pic']
            if pic:
                filename = secure_filename(str(user.id) + '.png')
                pic.save(
                    os.path.join(current_app.config['UPLOAD_DIR'], filename))

        except IntegrityError:
            flash('Username or email are already taken')

    # Show form
    return render_template('profile/edit.html',user=user)

#TODO
@profile.route()
@login_required
def subscriptions():
    """ Show list of subscriptions. """
    # Get user
    username = session.get('user', None)
    try:
        user = User.get(User.username == username)

    except User.DoesNotExist:
        abort(404)

    # Find subscriptions
    subs = (User
            .select()
            .join(Subscription, on=Subscription.publisher)
            .where(Subscription.subscriber == user)
            .order_by(User.username.asc()))

    try:
        #TODO
        # object_list
        return 

    except NotFound:
        # Prevent 404 and show nicer message
        return render_template('profile/subs.html',
                user=user,
                title='Subscriptions')

#TODO
@profile.route()
@login_required
def subscribers():
    """ Show list of subscriptions. """
    # Get user
    username = session.get('user', None)
    try:
        user = User.get(User.username == username)

    except User.DoesNotExist:
        abort(404)

    # Find followers
    subs = (User
            .select()
            .join(Subscription, on=Subscription.subscriber)
            .where(Subscription.publisher == user)
            .order_by(User.username.asc()))

    try:
        #TODO
        #object_list
        return 

    except NotFound:
        # Prevent 404 and show nicer message
        return render_template('profile/subs.html',
                user=user,
                title='Followers')
