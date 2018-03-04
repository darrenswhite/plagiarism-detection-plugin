import logging
from unittest import TestCase

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
