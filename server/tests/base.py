import logging
from functools import partial, wraps
from unittest import TestCase

from ldap3 import Server, Connection, MOCK_SYNC
from mock import patch

from server import server


class BaseTest(TestCase):
    """
    The base test case for unit tests
    """
    def setUp(self):
        """
        Set up the test
        """
        # Mock the server database
        self.mockdb = server.mockdb()
        # Setup the server but don't run it
        server.run(force_debug=True, run=False)
        # Get the Flask test client
        self.app = server.app.test_client()
        # Set the application to testing
        self.app.testing = True
        self.log = logging.getLogger(type(self).__name__)

    def tearDown(self):
        # Stop the mockupdb
        self.mockdb.stop()

    @staticmethod
    def patch_connection(f=None, gecos=None, bind=True):
        """
        Patch the LDAP connection
        :param f: The function to patch
        :param gecos: The gecos data to use
        :param bind: true if bind should be successful; false otherwise
        :return: The patched function wrapper
        """
        @patch('ldap3.core.connection.Connection.entries')
        @patch('ldap3.core.connection.Connection.search')
        @patch('ldap3.core.connection.Connection.bind')
        @patch('server.ldap.connection')
        @patch('server.ldap.server')
        @wraps(f)
        def wrapper(self, mock_server, mock_connection, mock_bind, mock_search,
                    mock_entries):
            # Create patched server
            server = Server('patched_server')
            mock_server.return_value = server
            # Create mocked connected
            mock_connection.return_value = Connection(server,
                                                      client_strategy=MOCK_SYNC)
            # Mock bind value
            mock_bind.return_value = bind
            # Mock search function
            mock_search.side_effect = self.search
            # Mock entries to return gecos
            mock_entries.__getitem__.return_value.__getitem__.return_value.value = \
                gecos
            return f(self)

        if f is None:
            return partial(BaseTest.patch_connection, gecos=gecos, bind=bind)

        return wrapper

    @staticmethod
    def search(*args, **kwargs):
        # Return gecos when requested
        if 'BASE' not in args \
                and 'attributes' in kwargs \
                and 'gecos' in kwargs['attributes']:
            return True
        else:
            return False
