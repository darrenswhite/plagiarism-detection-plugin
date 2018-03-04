from flask import url_for
from mock import patch
from mockupdb import go, Command

from server import server
from tests.base import BaseTest


class TestSignin(BaseTest):
    def search(*args, **kwargs):
        if 'BASE' not in args \
                and 'attributes' in kwargs \
                and 'gecos' in kwargs['attributes']:
            return True
        else:
            return False

    @patch('ldap3.core.connection.Connection.entries')
    @patch('ldap3.core.connection.Connection.search')
    @patch('ldap3.core.connection.Connection.bind')
    def test_first_time_signin(self, mock_bind, mock_search, mock_entries):
        mock_bind.return_value = True
        mock_search.side_effect = self.search
        mock_entries.__getitem__.return_value.__getitem__.return_value.value = \
            'John Smith,ADN,,,[ABUG]'

        future = go(self.app.post, '/', data={
            'uid': 'jos1',
            'password': 'abc123',
        })

        request = self.mockdb.receives(
            Command('find', 'submissions', filter={'uid': 'jos1'}))
        request.ok(cursor={'id': 0, 'firstBatch': [None]})
        request = self.mockdb.receives(
            Command('insert', 'submissions'))
        request.ok()

        documents = request['documents']

        self.assertEqual(1, len(documents))

        doc = documents[0]

        self.assertEqual('John Smith', doc['full_name'])
        self.assertEqual('jos1', doc['uid'])
        self.assertEqual('ABUG', doc['user_type'])
        self.assertEqual(0, len(doc['submissions']))

        response = future()

        self.assertEqual(response.status_code, 302)
        with server.app.test_request_context():
            self.assertEqual(response.location,
                             url_for('dashboard.overview', _external=True))

    @patch('ldap3.core.connection.Connection.entries')
    @patch('ldap3.core.connection.Connection.search')
    @patch('ldap3.core.connection.Connection.bind')
    def test_existing_signin(self, mock_bind, mock_search, mock_entries):
        mock_bind.return_value = True
        mock_search.side_effect = self.search
        mock_entries.__getitem__.return_value.__getitem__.return_value.value = \
            'John Smith,ADN,,,[ABUG]'

        future = go(self.app.post, '/', data={
            'uid': 'jos1',
            'password': 'abc123',
        })

        request = self.mockdb.receives(
            Command('find', 'submissions', filter={'uid': 'jos1'}))
        request.ok(cursor={'id': 0, 'firstBatch': [{'uid': 'jos1'}]})
        request = self.mockdb.receives(
            Command('update', 'submissions', updates=[{
                'q': {
                    'uid': 'jos1'
                },
                'u': {
                    '$set': {
                        'submissions': [],
                        'full_name': 'John Smith',
                        'uid': 'jos1',
                        'user_type': 'ABUG'
                    }
                },
                'multi': False,
                'upsert': False
            }]))
        request.ok()

        response = future()

        self.assertEqual(response.status_code, 302)
        with server.app.test_request_context():
            self.assertEqual(response.location,
                             url_for('dashboard.overview', _external=True))
