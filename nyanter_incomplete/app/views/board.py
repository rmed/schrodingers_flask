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
    # TODO
    nyas = 

    try:
        # TODO
        # object_list

    except NotFound:
        # Prevent 404 and show nicer message
        return render_template('board/nyas.html')

@board.route('/nyanters')
@login_required
def nyanters():
    """ Show a paginated list of users. """
    # All your nyanters are belong to us
    #TODO
    users = 

    try:
        # TODO
        # object_list

    except NotFound:
        # Prevent 404 and show nicer message
        return render_template('board/users.html')
