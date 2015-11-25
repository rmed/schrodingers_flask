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
@profile.route('/<username>')
@login_required
def show(username):
    """ Show a profile. """
    if not username:
        username = session.get('user', None)

    # Get user
    try:
        user = User.get(User.username == username)
        myself = User.get(User.username == session.get('user', None))

    except User.DoesNotExist:
        abort(404)

    # Check if following
    try:
        sub = Subscription.get(Subscription.subscriber == myself,
                Subscription.publisher == user)

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
        return object_list('profile/show.html',
                query=nyas,
                context_variable='nyas',
                paginate_by=10,
                user=user,
                is_following=is_following)

    except NotFound:
        # Prevent 404 and show nicer message
        return render_template('profile/show.html', user=user)

@profile.route('/new', methods=['GET', 'POST'])
@login_required
def new_nya():
    """ Publish a new Nya. """
    if request.method == 'POST':
        username = session.get('user', None)

        # Get user
        try:
            user = User.get(User.username == username)

        except User.DoesNotExist:
            abort(404)

        message = request.form['message'][0:160]

        # Create Nya
        nya = Nya.create(
                message=message,
                author=user)

        return redirect(url_for('profile.show'))

    # Show form
    return render_template('profile/new_nya.html')

@profile.route('/toggle-follow', defaults={'username': None})
@profile.route('/<username>/toggle-follow')
@login_required
@forbid_owner
def toggle_follow(username):
    """ (Un)Subscribe to another user. """
    # Get user
    try:
        user = User.get(User.username == username)
        myself = User.get(User.username == session.get('user', None))

    except User.DoesNotExist:
        abort(404)

    # Check if following
    try:
        sub = Subscription.get(Subscription.subscriber == myself,
                Subscription.publisher == user)

        # Exists
        is_following = True

    except Subscription.DoesNotExist:
        is_following = False


    if is_following:
        # Unfollow
        sub.delete_instance()

    else:
        # Follow
        Subscription.create(subscriber=myself, publisher=user)

    return redirect(url_for('profile.show', username=username))

@profile.route('/edit', methods=['GET', 'POST'])
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
        user.username = request.form['username']
        user.email = request.form['email']
        user.password = User.generate_password(request.form['password'])

        # Update user information
        try:
            user.save()

            flash('Success, changes saved')
            session['user'] = request.form['username']

            pic = request.files['pic']
            if pic:
                filename = secure_filename(str(user.id) + '.png')
                pic.save(
                    os.path.join(current_app.config['UPLOAD_DIR'], filename))

        except IntegrityError:
            flash('Username or email are already taken')

    # Show form
    return render_template('profile/edit.html',user=user)

@profile.route('/subscriptions')
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
        return object_list('profile/subs.html',
                query=subs,
                context_variable='subs',
                paginate_by=10,
                user=user,
                title='Subscriptions')

    except NotFound:
        # Prevent 404 and show nicer message
        return render_template('profile/subs.html',
                user=user,
                title='Subscriptions')

@profile.route('/followers')
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
        return object_list('profile/subs.html',
                query=subs,
                context_variable='subs',
                paginate_by=10,
                user=user,
                title='Followers')

    except NotFound:
        # Prevent 404 and show nicer message
        return render_template('profile/subs.html',
                user=user,
                title='Followers')
