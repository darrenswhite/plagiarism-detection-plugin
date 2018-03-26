import logging
import os

from postprocessor.db import SubmissionCollection
from postprocessor.fileprocessor import FileProcessor
from postprocessor.xml_parser import cipherparse


class PostProcessor:
    def __init__(self) -> None:
        super().__init__()
        self.log = logging.getLogger(type(self).__name__)

        # Submissions collection for the plagiarism database
        self.submissions = SubmissionCollection()

    def process(self, submission):
        self.log.info('Processing submission: {}'.format(submission))

        for path, data in submission.items():
            FileProcessor(path, data).process()

    def run(self, filename=None):
        """
        Set up logging and start the post processor
        """
        # Set PDP_DEBUG in the environment to enable debug
        # Use env instead of args because we are using Docker
        debug = 'PDP_DEBUG' in os.environ

        self.setup_logging(debug)

        if filename is None:
            self.watch()
        else:
            self.process(cipherparse(filename))

    @staticmethod
    def setup_logging(debug):
        """
        Configure logging with a custom format and debug logging
        :param debug: Set to True to enable debug logging
        """
        log_level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(format='%(levelname)-8s %(asctime)s: %(name)20s '
                                   '[%(filename)20s:%(lineno)-4s %(funcName)-20s] '
                                   '%(message)s', level=log_level)

    def watch(self):
        with self.submissions.watch() as stream:
            for change in stream:
                self.process(change)
