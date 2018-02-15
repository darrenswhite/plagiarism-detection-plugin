import logging
import os

from flask import Flask
from flask_login import LoginManager

from server.dashboard.views import dashboard
from server.db import SubmissionCollection, get_plagiarism_db

HOST = '0.0.0.0'
PORT = 8000

app = Flask(__name__)
app.config['SECRET_KEY'] = 'plagiarismdetectiondaw48'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'

from server.auth.views import auth

app.register_blueprint(auth)
app.register_blueprint(dashboard)

submissions = SubmissionCollection(get_plagiarism_db())


def _real_main():
    debug = os.environ.get('PDS_DEBUG', False)

    setup_logging(debug)

    app.run(host=HOST, port=PORT, debug=debug)


def main():
    try:
        _real_main()
    except KeyboardInterrupt:
        pass


def setup_logging(debug):
    log_level = logging.INFO

    if debug:
        log_level = logging.DEBUG

    logging.basicConfig(format='%(levelname)-8s %(asctime)s: %(name)20s '
                               '[%(filename)20s:%(lineno)-4s %(funcName)-20s] '
                               '%(message)s', level=log_level)
