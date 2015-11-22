from flask import session, redirect, url_for, request, abort
from functools import wraps

def login_required(f):
    """ Check if the user is logged in and redirect to login page
        if they are not logged in.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in', False) or not session.get('user', None):
            return redirect(url_for('home.login', next=request.url))

        return f(*args, **kwargs)
    return decorated_function

def forbid_owner(f):
    """ The route cannot be accessed by the logged in user because it belongs
        to them. Show a forbidden error.

        Call this after @login_required.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = request.view_args.get('username', None)
        if not username or username == session.get('user', None):
            # Nope nope nope
            abort(403)

        return f(*args, **kwargs)
    return decorated_function

def only_owner(f):
    """ The route can only be accessed by the logged in user
        (owner of the page). Show a forbidden error.

        Call this after @login_required.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.args.get('username', None) != session.get('user', None):
            # Nope nope nope
            abort(403)

        return f(*args, **kwargs)
    return decorated_function
