import logging
from functools import partial, wraps
from unittest import TestCase

from ldap3 import Server, Connection, MOCK_SYNC
from mock import patch

from server import server


class BaseTest(TestCase):
    def setUp(self):
        self.mockdb = server.mockdb()
        server.run(force_debug=True, run=False)
        self.app = server.app.test_client()
        self.app.testing = True
        self.log = logging.getLogger(type(self).__name__)

    def tearDown(self):
        self.mockdb.stop()

    @staticmethod
    def patch_connection(f=None, gecos=None, bind=True):
        @patch('ldap3.core.connection.Connection.entries')
        @patch('ldap3.core.connection.Connection.search')
        @patch('ldap3.core.connection.Connection.bind')
        @patch('server.ldap.connection')
        @patch('server.ldap.server')
        @wraps(f)
        def wrapper(self, mock_server, mock_connection, mock_bind, mock_search,
                    mock_entries):
            server = Server('patched_server')
            mock_server.return_value = server
            mock_connection.return_value = Connection(server,
                                                      client_strategy=MOCK_SYNC)
            mock_bind.return_value = bind
            mock_search.side_effect = self.search
            mock_entries.__getitem__.return_value.__getitem__.return_value.value = \
                gecos
            return f(self)

        if f is None:
            return partial(BaseTest.patch_connection, gecos=gecos, bind=bind)

        return wrapper

    @staticmethod
    def search(*args, **kwargs):
        if 'BASE' not in args \
                and 'attributes' in kwargs \
                and 'gecos' in kwargs['attributes']:
            return True
        else:
            return False
