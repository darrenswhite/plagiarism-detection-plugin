import logging

from flask import Blueprint, abort, render_template, request, flash, redirect
from flask_login import login_required, current_user

from server import app, submissions, xml_parser

# The dashboard blueprint, the index will be at /dashboard
dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

log = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = ['xml']


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

    # Try and submit the POST form submission
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part.', 'danger')
            return redirect(request.url)

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No file submitted.', 'danger')
            return redirect(request.url)

        # Check file extensions
        if file and valid_filename(file.filename):
            title = request.form.get('title')
            module = request.form.get('module')
            data = xml_parser.parse(file)
            # TODO Check if submission transaction was successful
            submissions.insert_one(current_user.uid, title, module, data,
                                   processed=False)
            flash('Submission saved successfully.', 'success')
        else:
            flash('Invalid file. File type must be xml.', 'danger')

    return render_template('dashboard/submit.html')


def valid_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[
        1].lower() in ALLOWED_EXTENSIONS
