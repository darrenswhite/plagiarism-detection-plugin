import logging
import unittest

from mock import patch

from server import app, real_main


class Test(unittest.TestCase):
    """
    TODO: Mock MongoDB
    """
    def setUp(self):
        real_main(force_debug=True, run=False)
        app.testing = True
        self.app = app.test_client()
        self.log = logging.getLogger(type(self).__name__)

    @patch('ldap3.core.connection.Connection.entries')
    @patch('ldap3.core.connection.Connection.search')
    @patch('ldap3.core.connection.Connection.bind')
    def test_signin(self, mock_bind, mock_search, mock_entries):
        def search(*args, **kwargs):
            if 'BASE' in args:
                return False
            else:
                return True

        mock_bind.return_value = True
        mock_search.side_effect = search
        mock_entries.return_value = [
            {
                'value': 'AUUD'
            }
        ]

        result = self.app.post('/', data={
            'uid': 'abc',
            'password': '123',
        })
        self.log.info(result)
        self.assertEqual(True, False)
