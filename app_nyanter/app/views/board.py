from flask import Blueprint, render_template, request, url_for, \
        redirect, session, flash
from playhouse.flask_utils import get_object_or_404, object_list
from peewee import IntegrityError
from werkzeug.exceptions import NotFound

from ..models import User, Nya
from ._util import login_required

board = Blueprint('board', __name__)

@board.route('/nyanboard')
@login_required
def nyanboard():
    """ Show a paginated list of nyas. """
    # All your nyas are belong to us
    nyas = (Nya
            .select(Nya, User)
            .join(User)
            .order_by(Nya.timestamp.desc())
            )

    try:
        return object_list('board/nyas.html',
                query=nyas,
                context_variable='nyas',
                paginate_by=40)

    except NotFound:
        # Prevent 404 and show nicer message
        return render_template('board/nyas.html')

@board.route('/nyanters')
@login_required
def nyanters():
    """ Show a paginated list of users. """
    # All your nyas are belong to us
    users = (User
            .select()
            .order_by(User.username.asc())
            )

    try:
        return object_list('board/users.html',
                query=users,
                context_variable='users',
                paginate_by=40)

    except NotFound:
        # Prevent 404 and show nicer message
        return render_template('board/users.html')
