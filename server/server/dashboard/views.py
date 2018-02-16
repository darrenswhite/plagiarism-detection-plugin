from flask import Blueprint, render_template
from flask_login import login_required, current_user

# The dashboard blueprint, the index will be at /dashboard
dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/')
@login_required
def index():
    """
    The dashboard index route for logged in users
    """
    print(current_user.get_card_type())
    if current_user.is_staff():
        return render_template('staff_dashboard.html')
    else:
        return render_template('student_dashboard.html')
