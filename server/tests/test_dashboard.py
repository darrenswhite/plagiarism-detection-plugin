import re

from flask import url_for
from mockupdb import go, Command

from server import server
from tests.base import BaseTest
from .test_data import AberUndergrad, AberStaff, AberUndergrad2


class TestDashboard(BaseTest):
    # Regex for student dashboard submissions table
    STUDENT_SUBMISSION_REGEX = '<tr>\s*<td>{}<\/td>\s*<td>{}<\/td>'
    # Regex for staff dashboard submissions table
    STAFF_SUBMISSION_REGEX = '<td>{}<\/td>\s*<td>{}<\/td>\s*<td>'

    @BaseTest.patch_connection(gecos=AberUndergrad.GECOS)
    def test_student_dashboard(self):
        future = go(self.app.post, '/', data={
            'uid': AberUndergrad.UID,
            'password': AberUndergrad.PASSWORD,
        })

        # Request to get current user
        request = self.mockdb.receives(
            Command('find', 'submissions', filter={'uid': AberUndergrad.UID}))
        # Send back user data
        request.ok(cursor={'id': 0, 'firstBatch': [
            {'uid': AberUndergrad.UID, 'full_name': AberUndergrad.FULL_NAME,
             'user_type': AberUndergrad.USER_TYPE}]})
        # Update user info upon login
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

        # Check dashboard redirection
        response = future()

        self.assertEqual(response.status_code, 302)

        with server.app.test_request_context():
            self.assertEqual(response.location,
                             url_for('dashboard.overview', _external=True))

        # Get the dashboard index
        future = go(self.app.get, '/dashboard/')

        # Expect request to find user
        request = self.mockdb.receives(
            Command('find', 'submissions', filter={'uid': AberUndergrad.UID}))
        # Send back user data
        request.ok(cursor={'id': 0, 'firstBatch': [
            {'uid': AberUndergrad.UID, 'full_name': AberUndergrad.FULL_NAME,
             'user_type': AberUndergrad.USER_TYPE}]})
        # Expect request to find user submissions
        request = self.mockdb.receives(
            Command('find', 'submissions', filter={'uid': AberUndergrad.UID}))
        # Send back user submissions
        request.ok(cursor={'id': 0, 'firstBatch': [
            {
                'submissions': AberUndergrad.SUBMISSIONS
            }
        ]})

        # Check submissions are in the dashboard table
        response = future()

        for s in AberUndergrad.SUBMISSIONS:
            regex = self.STUDENT_SUBMISSION_REGEX.format(s['title'],
                                                         s['module'])
            self.assertTrue(re.search(regex, response.get_data(as_text=True)))

    @BaseTest.patch_connection(gecos=AberStaff.GECOS)
    def test_staff_dashboard(self):
        future = go(self.app.post, '/', data={
            'uid': AberStaff.UID,
            'password': AberStaff.PASSWORD,
        })

        # Request to get current user
        request = self.mockdb.receives(
            Command('find', 'submissions', filter={'uid': AberStaff.UID}))
        # Send back user data
        request.ok(cursor={'id': 0, 'firstBatch': [
            {'uid': AberStaff.UID, 'full_name': AberStaff.FULL_NAME,
             'user_type': AberStaff.USER_TYPE}]})
        # Update user info upon login
        request = self.mockdb.receives(
            Command('update', 'submissions', updates=[{
                'q': {
                    'uid': AberStaff.UID
                },
                'u': {
                    '$set': {
                        'full_name': AberStaff.FULL_NAME,
                        'uid': AberStaff.UID,
                        'user_type': AberStaff.USER_TYPE
                    }
                },
                'multi': False,
                'upsert': False
            }]))
        request.ok()

        # Check dashboard redirection
        response = future()

        self.assertEqual(response.status_code, 302)

        with server.app.test_request_context():
            self.assertEqual(response.location,
                             url_for('dashboard.overview', _external=True))

        # Get the dashboard index
        future = go(self.app.get, '/dashboard/')

        # Expect request to find user
        request = self.mockdb.receives(
            Command('find', 'submissions', filter={'uid': AberStaff.UID}))
        # Send back user data
        request.ok(cursor={'id': 0, 'firstBatch': [
            {
                'uid': AberStaff.UID,
                'full_name': AberStaff.FULL_NAME,
                'user_type': AberStaff.USER_TYPE
            }
        ]})

        # Expect request to find all submissions
        request = self.mockdb.receives(
            Command('find', 'submissions'))
        # Send back all submissions
        request.ok(cursor={'id': 0, 'firstBatch': [
            {
                'uid': AberUndergrad.UID,
                'full_name': AberUndergrad.FULL_NAME,
                'user_type': AberUndergrad.USER_TYPE,
                'submissions': AberUndergrad.SUBMISSIONS
            },
            {
                'uid': AberUndergrad2.UID,
                'full_name': AberUndergrad2.FULL_NAME,
                'user_type': AberUndergrad2.USER_TYPE,
                'submissions': AberUndergrad2.SUBMISSIONS
            }
        ]})

        # Check submissions are in the dashboard table
        response = future()

        for s in AberUndergrad.SUBMISSIONS + AberUndergrad2.SUBMISSIONS:
            regex = self.STAFF_SUBMISSION_REGEX.format(s['title'],
                                                       s['module'])
            self.assertTrue(re.search(regex, response.get_data(as_text=True)))
