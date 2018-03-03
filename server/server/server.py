import logging
import os

from flask import Flask
from flask_login import LoginManager
from mockupdb import MockupDB

from server.auth.user import User
from server.db import SubmissionCollection


class Server:
    HOST = '0.0.0.0'
    PORT = 8000

    def __init__(self) -> None:
        super().__init__()
        self.app = Flask(__name__)
        # Secret key used for session data
        self.app.config['SECRET_KEY'] = 'plagiarismdetectiondaw48'
        # Setup Flask LoginManager
        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)
        # The index page will be the login view
        self.login_manager.login_view = '/'
        self.login_manager.user_loader(self.load_user)

        # Submissions collection for the plagiarism database
        self.submissions = SubmissionCollection()

    def load_user(self, uid):
        """
        Loads the User for given a uid
        :param uid: The User uid
        :return: A User object for the uid
        """
        user = self.submissions.find_user(uid)
        if user is None:
            return None
        else:
            return User(user['uid'], user['full_name'], user['user_type'])

    def mockdb(self):
        mockdb = MockupDB(auto_ismaster=True)
        mockdb.run()
        self.submissions = SubmissionCollection(uri=mockdb.uri)
        return mockdb

    def run(self, force_debug=False, run=True):
        """
        Set up logging and start the Flask application
        :param force_debug: Set to True to force enable debug logging
        :param run: Set to False to disable running the Flask application
        """
        # Set PDS_DEBUG in the environment to enable debug
        # Use env instead of args because we are using Docker
        # Set force_debug to True to override this
        debug = 'PDS_DEBUG' in os.environ or force_debug

        self.setup_logging(debug)

        from server.auth.views import auth
        # Register the auth for logging in/out via LDAP
        self.app.register_blueprint(auth)

        from server.dashboard.views import dashboard
        # Register the dashboard for logged in users
        self.app.register_blueprint(dashboard)

        if run:
            self.app.run(host=Server.HOST, port=Server.PORT, debug=debug)

    @staticmethod
    def setup_logging(debug):
        """
        Configure logging with a custom format and debug logging
        :param debug: Set to True to enable debug logging
        """
        log_level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(format='%(levelname)-8s %(asctime)s: %(name)20s '
                                   '[%(filename)20s:%(lineno)-4s %(funcName)-20s] '
                                   '%(message)s', level=log_level)
