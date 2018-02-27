import logging
import os

from flask import Flask
from flask_login import LoginManager

from server.auth.user import User
from server.db import SubmissionCollection, get_plagiarism_db

# Flask application options
HOST = '0.0.0.0'
PORT = 8000

app = Flask(__name__)
# Secret key used for session data
app.config['SECRET_KEY'] = 'plagiarismdetectiondaw48'

# Setup Flask LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
# The index page will be the login view
login_manager.login_view = '/'

# Submissions collection for the plagiarism database
submissions = SubmissionCollection(get_plagiarism_db())


def real_main(force_debug=False, run=True):
    """
    Set up logging and start the Flask application
    :param force_debug: Set to True to force enable debug logging
    :param run: Set to False to disable running the Flask application
    """
    # Set PDS_DEBUG in the environment to enable debug
    # Use env instead of args because we are using Docker
    # Set force_debug to True to override this
    debug = 'PDS_DEBUG' in os.environ or force_debug

    setup_logging(debug)

    from server.auth.views import auth
    # Register the auth for logging in/out via LDAP
    app.register_blueprint(auth)
    from server.dashboard.views import dashboard
    # Register the dashboard for logged in users
    app.register_blueprint(dashboard)

    if run:
        app.run(host=HOST, port=PORT, debug=debug)


@login_manager.user_loader
def load_user(uid):
    """
    Create a User given a uid
    :param uid: The User uid
    :return: A User object for the uid
    """
    user = submissions.find_user(uid)
    if user is None:
        return None
    else:
        return User(user['uid'], user['full_name'], user['user_type'])


def main():
    """
    Wrapper for the main function
    """
    try:
        real_main()
    except KeyboardInterrupt:
        pass


def setup_logging(debug):
    """
    Configure logging with a custom format and debug logging
    :param debug: Set to True to enable debug logging
    """
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(format='%(levelname)-8s %(asctime)s: %(name)20s '
                               '[%(filename)20s:%(lineno)-4s %(funcName)-20s] '
                               '%(message)s', level=log_level)
