import logging
import unittest

from mock import patch
from mockupdb import go, Command

from server import server


class TestSignin(unittest.TestCase):
    def setUp(self):
        self.mockdb = server.mockdb()
        server.run(force_debug=True, run=False)
        self.app = server.app.test_client()
        self.app.testing = True
        self.log = logging.getLogger(type(self).__name__)

    def tearDown(self):
        self.mockdb.stop()

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
        mock_entries.__getitem__.return_value.__getitem__.return_value.value = \
            'John Smith,ADN,,,[ABUG]'

        future = go(self.app.post, data={
            'uid': 'jos1',
            'password': 'abc123',
        })

        request = self.mockdb.receives(
            Command('find', 'submissions', filter={'uid': 'jos1'}))
        request.ok(cursor={'id': 0, 'firstBatch': [None]})
        request = self.mockdb.receives(
            Command('insert', 'submissions'))

        documents = request['documents']

        self.assertEqual(1, len(documents))

        doc = documents[0]

        self.assertEqual('John Smith', doc['full_name'])
        self.assertEqual('jos1', doc['uid'])
        self.assertEqual('ABUG', doc['user_type'])
        self.assertEqual(0, len(doc['submissions']))
