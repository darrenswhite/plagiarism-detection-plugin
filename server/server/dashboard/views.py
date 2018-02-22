import logging

from flask import Blueprint, abort, render_template, request
from flask_login import login_required, current_user

from server import app

# The dashboard blueprint, the index will be at /dashboard
dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

log = logging.getLogger(__name__)


@app.errorhandler(403)
def forbidden(error):
    log.error(error)
    return render_template('dashboard/403.html',
                           description=error.description), 403


@dashboard.route('/')
@login_required
def overview():
    """
    The dashboard index route for logged in users
    """
    if current_user.is_staff():
        return render_template('dashboard/staff.html')
    else:
        return render_template('dashboard/student.html')


@dashboard.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    if current_user.is_staff():
        abort(403, 'Staff members cannot post submissions.')
    else:
        # Try and submit the POST form submission
        if request.method == 'POST':
            log.debug(request.files)
            log.debug(request.form)
        return render_template('dashboard/submit.html')
