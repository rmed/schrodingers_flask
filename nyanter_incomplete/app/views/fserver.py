from flask import Blueprint, render_template, request, url_for, \
        redirect, session, flash, send_file, current_app
from playhouse.flask_utils import get_object_or_404, object_list
from peewee import IntegrityError

import os

fserver = Blueprint('fserver', __name__)

@fserver.route('/profile/<int:user_id>')
def profile_pic(user_id):
    """ Serve a profile picture.

        If user picture is not found, return default one.
    """
    fpath = os.path.join(current_app.config['UPLOAD_DIR'], str(user_id) + '.png')
    if  os.path.isfile(fpath):
        return send_file(fpath)

    else:
        return current_app.send_static_file('img/default_profile.png')
