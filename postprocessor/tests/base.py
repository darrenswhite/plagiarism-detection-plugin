import logging
from unittest import TestCase

from postprocessor import PostProcessor


class BaseTest(TestCase):
    def setUp(self):
        self.pp = PostProcessor()
        self.mockdb = self.pp.mockdb()
        self.log = logging.getLogger(type(self).__name__)

    def tearDown(self):
        self.mockdb.stop()
