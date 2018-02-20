from flask import Blueprint, render_template
from flask_login import login_required, current_user

# The dashboard blueprint, the index will be at /dashboard
dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


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


@dashboard.route('/submit')
@login_required
def submit():
    if current_user.is_staff():
        pass
    else:
        return render_template('dashboard/submit.html')
