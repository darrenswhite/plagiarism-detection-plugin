import logging
from unittest import TestCase

from postprocessor import PostProcessor


class BaseTest(TestCase):
    """
    The base test case for unit tests
    """

    def setUp(self):
        # Create the post processor
        self.pp = PostProcessor()
        # Mock the post processor database
        self.mockdb = self.pp.mockdb()
        self.log = logging.getLogger(type(self).__name__)

    def tearDown(self):
        # Stop the mockupdb
        self.mockdb.stop()
