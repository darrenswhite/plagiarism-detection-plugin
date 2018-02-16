from flask import Blueprint, render_template
from flask_login import login_required

# The dashboard blueprint, the index will be at /dashboard
dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/')
@login_required
def index():
    """
    The dashboard index route for logged in users
    """
    return render_template('dashboard.html')
