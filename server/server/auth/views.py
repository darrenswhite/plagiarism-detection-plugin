import logging

from flask import request, render_template, flash, redirect, \
    url_for, Blueprint
from flask_login import current_user, login_user, \
    logout_user, login_required

from server import server
from server.ldap import try_bind

# The auth blueprint for the Flask app
auth = Blueprint('auth', __name__)

log = logging.getLogger(__name__)


@auth.route('/', methods=['GET', 'POST'])
def index():
    """
    The index page to allow users to login
    :return:
    """
    # Redirect to dashboard if user is logged in already
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.overview'))

    # Try and login with the POST form
    if request.method == 'POST':
        uid = request.form.get('uid')
        password = request.form.get('password')
        remember = request.form.get('remember-me') is not None

        # Try and login the user
        user = try_bind(uid, password)

        # Login failed
        if user is None:
            # TODO Add more specific error messages
            flash('Invalid username or password. Please try again.',
                  'danger')
            return render_template('index.html')

        log.debug('Current user: %s', user)
        # Login successful so update database with user info
        server.submissions.insert_user(user)
        # Login the user using flask_login
        login_user(user, remember=remember)
        flash('You have successfully logged in.', 'success')
        # Redirect to dashboard
        return redirect(url_for('dashboard.overview'))

    # Show index of the signin
    return render_template('index.html')


@auth.route('/logout')
@login_required
def logout():
    """
    Logout the current user
    """
    logout_user()
    return redirect(url_for('auth.index'))
