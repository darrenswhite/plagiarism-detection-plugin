from flask import request, render_template, flash, redirect, \
    url_for, Blueprint, g
from flask_login import current_user, login_user, \
    logout_user, login_required

from server import login_manager
from server.auth.user import User

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(uid):
    return User(uid)


@auth.before_request
def get_current_user():
    g.user = current_user


@auth.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        uid = request.form.get('uid')
        password = request.form.get('password')
        remember = request.form.get('remember-me') is not None

        if not User.try_login(uid, password):
            flash('Invalid username or password. Please try again.',
                  'danger')
            return render_template('index.html')

        user = load_user(uid)
        login_user(user, remember=remember)
        flash('You have successfully logged in.', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('index.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))
