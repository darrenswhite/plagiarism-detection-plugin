import logging
import os

from flask import Flask
from flask_login import LoginManager

from server.dashboard.views import dashboard
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

# This import is here because login_manager must exist first
from server.auth.views import auth

# Register the auth for logging in/out via LDAP
app.register_blueprint(auth)
# Register the dashboard for logged in users
app.register_blueprint(dashboard)

# Submissions collection for the plagiarism database
submissions = SubmissionCollection(get_plagiarism_db())


def _real_main():
    """
    Set up logging and start the Flask application
    """
    # Set PDS_DEBUG in the environment to enable debug
    # Use env instead of args because we are using Docker
    debug = 'PDS_DEBUG' in os.environ

    setup_logging(debug)

    app.run(host=HOST, port=PORT, debug=debug)


def main():
    """
    Wrapper for the main function
    """
    try:
        _real_main()
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
