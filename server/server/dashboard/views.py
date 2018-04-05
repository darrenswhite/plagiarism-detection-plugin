import logging

import bson
from bson.objectid import ObjectId
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
_SOURCES = ['Total', 'Clipboard', 'External', 'Other']

# Elements match _SOURCES
_SOURCES_COLORS = ['#000000', '#FF0000', '#00FF00', '#777777']


def __build_submission_scatter_chart(fts_data):
    """
    Builds the Frequency vs. Time scatter chart for a submission
    :param fts_data: The frequency time source data to plot
    :return: A Pygal XY chart
    """
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

    # Plot each source as a scatter plot using its color
    # Plot TOTAL data as a line with no dots
    for source in _SOURCES:
        data = [(r['t'], r['f']) for r in fts_data if
                r['s'] == source.upper() or source == 'Total']
        if source == 'Total':
            scatter_chart.add(source, data, show_dots=False, stroke=True)
        else:
            scatter_chart.add(source, data, show_dots=True, dots_size=1.5,
                              stroke=False)

    return scatter_chart


def __expand_submission(submission, user):
    """
    Adds extra data to the submission for viewing

    :param submission: The submission to add extra data to
    :param user: The user who owns the submission
    :return: The modified submission
    """
    result = submission.get('result', {})
    merged_result = __get_merged_result(result)
    merged_fts_data = merged_result.get('frequency_time_source_data', {})

    # Add user full name
    submission['full_name'] = user['full_name']

    # Add user uid
    submission['uid'] = user['uid']

    # Add scatter chart
    submission['scatter_chart'] = __build_submission_scatter_chart(
        merged_fts_data)

    if len(merged_fts_data) > 0:
        # Add total time
        submission['total_time'] = int(
            merged_fts_data[len(merged_fts_data) - 1]['t']) - int(
            merged_fts_data[0]['t'])

    # Add source frequencies
    for source in _SOURCES:
        key = 'frequency_' + source.lower()
        if key in merged_result:
            submission[key] = merged_result[key]

    return submission


@dashboard.errorhandler(403)
def forbidden(error):
    """
    Custom 403 error handler page
    :param error: The error that occured
    """
    log.error(error)
    return render_template('dashboard/error_handler.html',
                           description=error.description), 403


@dashboard.errorhandler(404)
def forbidden(error):
    """
    Custom 404 error handler page
    :param error: The error that occured
    """
    log.error(error)
    return render_template('dashboard/error_handler.html',
                           description=error.description), 404


def __get_merged_result(result):
    """
    Merge submission post-processed file results
    :param result: Post-processed submission result
    :return: Merged file result
    """
    merged_result = {}

    # Merge all fts data from each file to make one data set
    for path, data in result.items():
        for key, value in data.items():
            if key in merged_result:
                merged_result[key] += value
            else:
                merged_result[key] = value

    if 'frequency_time_source_data' in merged_result:
        # Sort fts data by time
        merged_result['frequency_time_source_data'] = sorted(
            merged_result['frequency_time_source_data'],
            key=lambda d: int(d['t']))

    return merged_result


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
    """
    The staff dashboard overview
    """
    # Find all users' submissions
    all_user_data = list(server.submissions.find())
    all_user_submissions = []

    # Add name to each submission
    for user in all_user_data:
        submissions = user['submissions']
        for s in submissions:
            __expand_submission(s, user)
        all_user_submissions.append(submissions)

    squashed_submissions = []

    # Squash all submissions into a single list
    for user_submissions in all_user_submissions:
        for s in user_submissions:
            squashed_submissions.append(s)

    return render_template('dashboard/staff.html',
                           submissions=squashed_submissions)


def __overview_student():
    """
    The student dashboard overview
    :return:
    """
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


@dashboard.route('/submission/<user_uid>/<submission_id>')
@login_required
def view_submission(user_uid, submission_id):
    """
    Route to view a submission details
    :param user_uid: The user uid that owns the submission
    :param submission_id: The submission id to view
    """
    # Only staff can view submission details
    if not current_user.is_staff():
        abort(403, 'Only staff members can view submission details.')

    user_data = server.submissions.find(
        {'uid': user_uid}).next()
    user_submissions = user_data['submissions'] if user_data else []
    match_submissions = []

    try:
        match_submissions = [s for s in user_submissions if
                             s['_id'] == ObjectId(submission_id)]
    except bson.errors.InvalidId:
        abort(404, 'Invalid submission id.')

    if len(match_submissions) == 0:
        abort(404, 'Submission not found.')

    # Add extra info to the submission
    submission = match_submissions[0]

    __expand_submission(submission, user_data)

    return render_template('dashboard/submission.html', submission=submission,
                           sources=_SOURCES)
