import functools
import re

from flask import url_for
from mock import patch
from mockupdb import go, Command

from server import server
from server.auth.user import User
from tests.base import BaseTest
from .test_data import AberUndergrad, AberStaff


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
    @patch_connection(gecos=AberUndergrad.GECOS)
    def test_existing_signin(self):
        future = go(self.app.post, '/', data={
            'uid': AberUndergrad.UID,
            'password': AberUndergrad.PASSWORD,
        })

        request = self.mockdb.receives(
            Command('find', 'submissions', filter={'uid': AberUndergrad.UID}))
        request.ok(cursor={'id': 0, 'firstBatch': [{'uid': AberUndergrad.UID}]})
        request = self.mockdb.receives(
            Command('update', 'submissions', updates=[{
                'q': {
                    'uid': AberUndergrad.UID
                },
                'u': {
                    '$set': {
                        'full_name': AberUndergrad.FULL_NAME,
                        'uid': AberUndergrad.UID,
                        'user_type': AberUndergrad.USER_TYPE
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

    @patch_connection(gecos=AberUndergrad.GECOS)
    def test_first_time_signin(self):
        future = go(self.app.post, '/', data={
            'uid': AberUndergrad.UID,
            'password': AberUndergrad.PASSWORD,
        })

        request = self.mockdb.receives(
            Command('find', 'submissions', filter={'uid': AberUndergrad.UID}))
        request.ok(cursor={'id': 0, 'firstBatch': [None]})
        request = self.mockdb.receives(
            Command('insert', 'submissions'))
        request.ok()

        documents = request['documents']

        self.assertEqual(1, len(documents))

        doc = documents[0]

        self.assertEqual(AberUndergrad.FULL_NAME, doc['full_name'])
        self.assertEqual(AberUndergrad.UID, doc['uid'])
        self.assertEqual(AberUndergrad.USER_TYPE, doc['user_type'])
        self.assertEqual(0, len(doc['submissions']))

        response = future()

        self.assertEqual(response.status_code, 302)

        with server.app.test_request_context():
            self.assertEqual(response.location,
                             url_for('dashboard.overview', _external=True))

    @patch_connection(bind=False)
    def test_invalid_signin(self):
        response = self.app.post('/', data={
            'uid': AberUndergrad.UID,
            'password': AberUndergrad.PASSWORD,
        })

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            re.search('Invalid username or password. Please try again.',
                      response.get_data(as_text=True)))

    def test_user_staff(self):
        user = User(AberStaff.UID, AberStaff.FULL_NAME,
                    AberStaff.USER_TYPE)

        self.assertEqual(user.get_card_type(), AberStaff.CARD_TYPE)
        self.assertEqual(user.get_id(), AberStaff.UID)
        self.assertEqual(user.is_staff(), True)

    def test_user_student(self):
        user = User(AberUndergrad.UID, AberUndergrad.FULL_NAME,
                    AberUndergrad.USER_TYPE)

        self.assertEqual(user.get_card_type(), AberUndergrad.CARD_TYPE)
        self.assertEqual(user.get_id(), AberUndergrad.UID)
        self.assertEqual(user.is_staff(), False)
