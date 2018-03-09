import functools
import re

from flask import url_for
from mock import patch
from mockupdb import go, Command

from server import server
from tests.base import BaseTest


def patch_connection(f=None, gecos=None, bind=True):
    if f is None:
        return functools.partial(patch_connection, gecos=gecos, bind=bind)

    @patch('ldap3.core.connection.Connection.entries')
    @patch('ldap3.core.connection.Connection.search')
    @patch('ldap3.core.connection.Connection.bind')
    @functools.wraps(f)
    def wrapper(self, mock_bind, mock_search, mock_entries):
        mock_bind.return_value = bind
        mock_search.side_effect = search
        mock_entries.__getitem__.return_value.__getitem__.return_value.value = \
            gecos
        return f(self)

    return wrapper


def search(*args, **kwargs):
    if 'BASE' not in args \
            and 'attributes' in kwargs \
            and 'gecos' in kwargs['attributes']:
        return True
    else:
        return False


class TestSignin(BaseTest):
    FULL_NAME = 'John Smith'
    USER_TYPE = 'ABUG'
    GECOS = '{},ADN,,,[{}]'.format(FULL_NAME, USER_TYPE)
    UID = 'jos1'
    PASSWORD = 'abc123'

    @patch_connection(gecos=GECOS)
    def test_first_time_signin(self):
        future = go(self.app.post, '/', data={
            'uid': self.UID,
            'password': self.PASSWORD,
        })

        request = self.mockdb.receives(
            Command('find', 'submissions', filter={'uid': self.UID}))
        request.ok(cursor={'id': 0, 'firstBatch': [None]})
        request = self.mockdb.receives(
            Command('insert', 'submissions'))
        request.ok()

        documents = request['documents']

        self.assertEqual(1, len(documents))

        doc = documents[0]

        self.assertEqual(self.FULL_NAME, doc['full_name'])
        self.assertEqual(self.UID, doc['uid'])
        self.assertEqual(self.USER_TYPE, doc['user_type'])
        self.assertEqual(0, len(doc['submissions']))

        response = future()

        self.assertEqual(response.status_code, 302)

        with server.app.test_request_context():
            self.assertEqual(response.location,
                             url_for('dashboard.overview', _external=True))

    @patch_connection(gecos=GECOS)
    def test_existing_signin(self):
        future = go(self.app.post, '/', data={
            'uid': self.UID,
            'password': self.PASSWORD,
        })

        request = self.mockdb.receives(
            Command('find', 'submissions', filter={'uid': self.UID}))
        request.ok(cursor={'id': 0, 'firstBatch': [{'uid': self.UID}]})
        request = self.mockdb.receives(
            Command('update', 'submissions', updates=[{
                'q': {
                    'uid': self.UID
                },
                'u': {
                    '$set': {
                        'full_name': self.FULL_NAME,
                        'uid': self.UID,
                        'user_type': self.USER_TYPE
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

    @patch_connection(bind=False)
    def test_invalid_signin(self):
        response = self.app.post('/', data={
            'uid': self.UID,
            'password': self.PASSWORD,
        })

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            re.search('Invalid username or password. Please try again.',
                      response.get_data(as_text=True)))
