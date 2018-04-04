import re

from flask import url_for
from mockupdb import go, Command

from server import server
from server.auth.user import User
from tests.base import BaseTest
from .test_data import AberUndergrad, AberStaff


class TestSignin(BaseTest):
    @BaseTest.patch_connection(gecos=AberUndergrad.GECOS)
    def test_existing_signin(self):
        # Send request in background
        future = go(self.app.post, '/', data={
            'uid': AberUndergrad.UID,
            'password': AberUndergrad.PASSWORD,
        })

        # A request is received to check if the user exists
        request = self.mockdb.receives(
            Command('find', 'submissions', filter={'uid': AberUndergrad.UID}))
        # Send back existing user
        request.ok(cursor={'id': 0, 'firstBatch': [
            {
                'uid': AberUndergrad.UID,
                'full_name': AberUndergrad.FULL_NAME,
                'user_type': AberUndergrad.USER_TYPE
            }
        ]})
        # User exists so we expect an update
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
        # Request is done
        request.ok()

        # Get the request response
        response = future()

        # We expect to be redirected to dashboard
        self.assertEqual(response.status_code, 302)

        with server.app.test_request_context():
            self.assertEqual(response.location,
                             url_for('dashboard.overview', _external=True))

    @BaseTest.patch_connection(gecos=AberUndergrad.GECOS)
    def test_first_time_signin(self):
        # Send request in background
        future = go(self.app.post, '/', data={
            'uid': AberUndergrad.UID,
            'password': AberUndergrad.PASSWORD,
        })

        # A request is received to check if the user exists
        request = self.mockdb.receives(
            Command('find', 'submissions', filter={'uid': AberUndergrad.UID}))
        # No user exists
        request.ok(cursor={'id': 0, 'firstBatch': [None]})
        # A new User should be inserted
        request = self.mockdb.receives(
            Command('insert', 'submissions'))
        # Request is done
        request.ok()

        # Only one user should be inserted
        documents = request['documents']

        self.assertEqual(1, len(documents))

        # Check the inserted user data
        doc = documents[0]

        self.assertEqual(AberUndergrad.FULL_NAME, doc['full_name'])
        self.assertEqual(AberUndergrad.UID, doc['uid'])
        self.assertEqual(AberUndergrad.USER_TYPE, doc['user_type'])
        self.assertEqual(0, len(doc['submissions']))

        # Check we are redirected to dashboard
        response = future()

        self.assertEqual(response.status_code, 302)

        with server.app.test_request_context():
            self.assertEqual(response.location,
                             url_for('dashboard.overview', _external=True))

    @BaseTest.patch_connection(bind=False)
    def test_invalid_signin(self):
        # Send request in background
        response = self.app.post('/', data={
            'uid': AberUndergrad.UID,
            'password': AberUndergrad.PASSWORD + 'wrong',
        })

        # Check we are not logged in
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            re.search('Invalid username or password. Please try again.',
                      response.get_data(as_text=True)))

    def test_user_staff(self):
        # Check gecos parsing
        user = User(AberStaff.UID, AberStaff.FULL_NAME,
                    AberStaff.USER_TYPE)

        self.assertEqual(user.get_card_type(), AberStaff.CARD_TYPE)
        self.assertEqual(user.get_id(), AberStaff.UID)
        self.assertEqual(user.is_staff(), True)

    def test_user_student(self):
        # Check gecos parsing
        user = User(AberUndergrad.UID, AberUndergrad.FULL_NAME,
                    AberUndergrad.USER_TYPE)

        self.assertEqual(user.get_card_type(), AberUndergrad.CARD_TYPE)
        self.assertEqual(user.get_id(), AberUndergrad.UID)
        self.assertEqual(user.is_staff(), False)
