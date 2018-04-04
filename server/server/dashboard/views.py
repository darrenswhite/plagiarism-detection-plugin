import logging

from flask import Blueprint, abort, render_template, request, flash, redirect
from flask_login import login_required, current_user
from pygal.graph.xy import XY
from pygal.style import Style

from server import server, xml_parser
from server.cipher import AESCipher

# The dashboard blueprint, the index will be at /dashboard
dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

cipher = AESCipher('plagiarismplugin')

log = logging.getLogger(__name__)

# Only allow uploading on XML files
ALLOWED_EXTENSIONS = ['xml']

# Source values for charts
_SOURCES = ['CLIPBOARD', 'EXTERNAL', 'OTHER']

# First element is for the line
# Other elements match _SOURCES
_SOURCES_COLORS = ['#000000', '#FF0000', '#00FF00', '#777777']


def __build_submission_scatter_chart(result):
    merged_fts_data = []

    # Merge all fts data from each file to make one data set
    for p, r in result.items():
        if 'frequency_time_source_data' in r:
            merged_fts_data += r['frequency_time_source_data']

    # Sort fts data by time
    merged_fts_data = sorted(merged_fts_data,
                             key=lambda d: int(d['t']))

    # Create a scatter chart for the data
    scatter_chart = XY(disable_xml_declaration=True,
                       legend_at_bottom=True,
                       legend_at_bottom_columns=len(_SOURCES_COLORS)
                       )
    scatter_chart.style = Style(
        background='transparent',
        plot_background='transparent',
        colors=_SOURCES_COLORS
    )
    scatter_chart.title = 'Character Frequency vs. Time'
    scatter_chart.x_title = 'Time (ms)'
    scatter_chart.y_title = 'Frequency'

    # Plot all data as a line
    data = [(r['t'], r['f']) for r in merged_fts_data]
    scatter_chart.add('ALL', data, show_dots=False)

    # Plot each source as a scatter plot using its color
    for source in _SOURCES:
        data = [(r['t'], r['f']) for r in merged_fts_data if
                r['s'] == source]
        scatter_chart.add(source, data, stroke=False)

    return scatter_chart


@dashboard.errorhandler(403)
def forbidden(error):
    """
    Custom 403 error handler page
    :param error: The error that occured
    """
    log.error(error)
    return render_template('dashboard/403.html',
                           description=error.description), 403


@dashboard.route('/')
@login_required
def overview():
    """
    The dashboard index route for logged in users
    """
    # Show staff or student dashboard depending on user
    if current_user.is_staff():
        return __overview_staff()
    else:
        return __overview_student()


def __overview_staff():
    # Find all users' submissions
    all_user_data = list(server.submissions.find())
    all_user_submissions = []

    # Add name to each submission
    for user in all_user_data:
        submissions = user['submissions']
        for s in submissions:
            s['full_name'] = user['full_name']

            # Add scatter chart if the submission has been processed
            if 'result' in s:
                s['scatter_chart'] = __build_submission_scatter_chart(
                    s['result'])
        all_user_submissions.append(submissions)

    squashed_submissions = []

    # Squash all submissions into a single list
    for user_submissions in all_user_submissions:
        for s in user_submissions:
            squashed_submissions.append(s)

    return render_template('dashboard/staff.html',
                           submissions=squashed_submissions)


def __overview_student():
    # Find all of the current users' submissions
    user_data = server.submissions.find(
        {'uid': current_user.uid}).next()
    user_submissions = user_data['submissions'] if user_data else []
    return render_template('dashboard/student.html',
                           submissions=user_submissions)


@dashboard.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    """
    The submission page to post new submissions
    """
    # Only students can post submissions
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
            # Decrypt the XML data
            data = xml_parser.cipherparse(file)
            # TODO Check if submission transaction was successful
            # Add submission to database
            server.submissions.insert_one(current_user.uid, title, module, data)
            flash('Submission saved successfully.', 'success')
        else:
            flash('Invalid file. File type must be xml.', 'danger')

    return render_template('dashboard/submit.html')


def valid_filename(filename):
    # Check valid extensions
    return '.' in filename and filename.rsplit('.', 1)[
        1].lower() in ALLOWED_EXTENSIONS
