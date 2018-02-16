import logging

from flask import request, render_template, flash, redirect, \
    url_for, Blueprint
from flask_login import current_user, login_user, \
    logout_user, login_required

from server import submissions
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
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    # Try and login with the POST form
    if request.method == 'POST':
        uid = request.form.get('uid')
        password = request.form.get('password')
        remember = request.form.get('remember-me') is not None

        user = try_bind(uid, password)

        if user is None:
            flash('Invalid username or password. Please try again.',
                  'danger')
            return render_template('index.html')

        log.debug('Current user: %s', user)
        submissions.insert_user(user)
        login_user(user, remember=remember)
        flash('You have successfully logged in.', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('index.html')


@auth.route('/logout')
@login_required
def logout():
    """
    Logout the current user
    """
    logout_user()
    return redirect(url_for('auth.index'))
