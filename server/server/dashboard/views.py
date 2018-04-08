import logging
import sys

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
__ALLOWED_EXTENSIONS = ['xml']

# Source values for charts
__SOURCES = ['Total', 'Clipboard', 'External', 'Other']

# Elements match _SOURCES
__SOURCES_COLORS = ['#000000', '#FF0000', '#00FF00', '#777777']

# P value maximum value
__P_VALUE_LIMIT = 40

# Size of a change to be considered "large"
__LARGE_CHANGE_FREQUENCY = 200


def __build_submission_scatter_chart(fts_data):
    """
    Builds the Frequency vs. Time scatter chart for a submission
    :param fts_data: The frequency time source data to plot
    :return: A Pygal XY chart
    """
    # Create a scatter chart for the data
    scatter_chart = XY(
        legend_at_bottom=True,
        legend_at_bottom_columns=len(__SOURCES_COLORS)
    )
    scatter_chart.style = Style(
        background='transparent',
        plot_background='transparent',
        colors=__SOURCES_COLORS
    )
    scatter_chart.title = 'Character Frequency vs. Time'
    scatter_chart.x_title = 'Time (minutes)'
    scatter_chart.y_title = 'Frequency'

    initial_t = fts_data[0]['t']
    # Normalise timestamps
    for r in fts_data:
        r['t'] -= initial_t

    # Plot each source as a scatter plot using its color
    # Plot Total source as a line with no dots
    for source in __SOURCES:
        data = [(r['t'] / 1000 / 60, r['f']) for r in fts_data if
                r['s'] == source.upper() or source == 'Total']
        if source == 'Total':
            scatter_chart.add(source, data, show_dots=False, stroke=True)
        else:
            scatter_chart.add(source, data, show_dots=True, dots_size=1.5,
                              stroke=False)

    return scatter_chart.render_data_uri()


def __calculate_p_color(p_value):
    """
    Calculates the color for the given p value
    :param p_value: The p value to calculate the color of
    :return: The p value color
    """
    # Mod is the max value for red
    # i.e when p_value = 0 p_color = green
    # and when p_value = 40 p_color = red
    mod = 255 / __P_VALUE_LIMIT
    r = min(255, round(p_value * mod))
    g = max(0, 255 - round(p_value * mod))
    return '#{:02X}{:02X}{:02X}'.format(r, g, 0)


def __calculate_p_value(submission):
    """
    Calculates the p value for the submission
    :param submission: The submission to calculate the p value of
    :return: The calulcated p value
    """
    # Get frequencies as float (0.0 - 1.0)
    clipboard_f = submission['frequency_clipboard'] / submission[
        'frequency_total']
    external_f = submission['frequency_external'] / submission[
        'frequency_total']
    cpm = submission['cpm']
    diff_ratio = submission['diff_ratio']
    # Ensure frequencies are minimum of 1
    # External has a significant impact
    # CPM acts as penalty modifier
    # Diff ratio acts as accuracy modifier
    return ((clipboard_f + 1) + pow(external_f + 1, 2)) * \
           (cpm / 100) * diff_ratio


def __expand_submission(submission, user, chart=False, large_changes=False,
                        normalise_changes=False, include_change_path=False):
    """
    Adds extra data to the submission for viewing

    :param submission: The submission to add extra data to
    :param user: The user who owns the submission
    :param chart: True to include the Pygal chart; false otherwise
    :param large_changes: True to include a list of large changes; false
    otherwise
    :param normalise_changes: True to normalise change timestamps; false
    otherwise
    :param include_change_path: True to include the file path for each change
    :return: The modified submission
    """
    result = submission.get('result', {})
    merged_result = __get_merged_result(result)
    merged_fts_data = merged_result.get('frequency_time_source_data', {})

    # Add user full name
    submission['full_name'] = user['full_name']

    # Add user uid
    submission['uid'] = user['uid']

    if chart:
        # Add scatter chart
        submission['scatter_chart'] = __build_submission_scatter_chart(
            merged_fts_data)

    if large_changes:
        # Add large changes
        submission['large_changes'] = \
            __get_changes(submission, __LARGE_CHANGE_FREQUENCY,
                          normalise=normalise_changes,
                          include_path=include_change_path)

    if len(merged_fts_data) > 0:
        # Add total time
        submission['total_time'] = int(
            merged_fts_data[len(merged_fts_data) - 1]['t']) - int(
            merged_fts_data[0]['t'])
    else:
        submission['total_time'] = -1

    # Add source frequencies
    for source in __SOURCES:
        key = 'frequency_' + source.lower()
        submission[key] = merged_result.get(key, -1)

    if 'frequency_total' in submission and 'total_time' in submission:
        # Add cpm (characters per minute)
        # Total time is in ms so convert to minutes
        submission['cpm'] = round(int(submission['frequency_total']) / (int(
            submission['total_time']) / 1000 / 60))
    else:
        submission['cpm'] = -1

    if 'diff_ratio' in merged_result:
        submission['diff_ratio'] = merged_result['diff_ratio'] / len(
            result.keys())
    else:
        submission['diff_ratio'] = -1

    p_value = __calculate_p_value(submission)
    submission['p_value'] = p_value
    submission['p_color'] = __calculate_p_color(p_value)

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


def __get_changes(submission, min_size=0, normalise=False, include_path=False):
    """
    Gets all the changes in a submission
    :param submission: The submission to get the changes from
    :param min_size: The minimum size a change must be
    :param normalise: True to normalise change timestamps; false otherwise
    :param include_path: True to include the file path for each change; false
    otherwise
    :return: A list of changes
    """
    changes = []
    # The initial timestamp used for normalising timestamps
    initial_t = sys.maxsize

    if normalise:
        # Find initial timestamp from all changes
        for path, data in submission['files'].items():
            for c in data['changes']:
                t = int(c['timestamp'])
                if t < initial_t:
                    initial_t = t
    else:
        # Set to zero if we're not normalising
        initial_t = 0

    for path, data in submission['files'].items():
        for c in data['changes']:
            size = abs(len(c['newString']) - len(c['oldString']))
            if size >= min_size:
                # No need to check normalise here as initial_t will be 0
                c['timestamp'] = int(c['timestamp']) - initial_t
                if include_path:
                    c['path'] = path
                changes.append(c)

    return changes


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
        1].lower() in __ALLOWED_EXTENSIONS


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

    __expand_submission(submission, user_data, chart=True, large_changes=True,
                        normalise_changes=True, include_change_path=True)

    return render_template('dashboard/submission.html', submission=submission,
                           sources=__SOURCES)
