import base64
import logging
import os
from difflib import SequenceMatcher

from postprocessor.changeprocessor import ChangeProcessor
from postprocessor.db import SubmissionCollection
from postprocessor.xml_parser import cipherparse


class PostProcessor:
    def __init__(self, plot=False) -> None:
        super().__init__()
        self.log = logging.getLogger(type(self).__name__)
        self.plot = plot
        # Submissions collection for the plagiarism database
        self.submissions = SubmissionCollection()

    @staticmethod
    def __build_document(changes):
        document = ''

        for c in changes:
            # get change data
            old_str = c['oldString']
            new_str = c['newString']
            offset = int(c['offset'])

            # Get the start and end of the document which shouldn't be modified
            start = document[:offset] if len(document) > 0 else ''
            end = document[offset + len(old_str):] if len(document) > 0 else ''

            # Insert the new value into the document
            document = start + new_str + end

        return document

    def __process(self, submission):
        self.log.info('Processing submission: {}'.format(submission))

        all_changes = []
        document_diff_ratios = {}

        for path, data in submission.items():
            changes = data['changes']
            # Ensure changes are sorted by timestamp
            data['changes'] = self.__sort_changes(changes)
            all_changes += changes

            # Deocde the document cache
            cache = base64.b64decode(data['cache']).decode('utf-8')
            # Reconstruct the document from the list of changes
            built = self.__build_document(changes)
            # Get the diff ratio between the cache and reconstructed document
            ratio = SequenceMatcher(None, cache, built).ratio()

            document_diff_ratios[path] = ratio

        # Sort all changes again
        all_changes = self.__sort_changes(all_changes)
        result = ChangeProcessor(all_changes, self.plot).process()
        # Add the document diff ratios to the final result
        result['document_diff_ratios'] = document_diff_ratios

        self.log.info('Result: {}'.format(result))

    def run(self, filename=None, ):
        """
        Set up logging and start the post processor
        """
        # Set PDP_DEBUG in the environment to enable debug
        # Use env instead of args because we are using Docker
        debug = 'PDP_DEBUG' in os.environ

        self.setup_logging(debug)

        if filename is None:
            self.__watch()
        else:
            self.__process(cipherparse(filename))

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

    @staticmethod
    def __sort_changes(changes):
        return sorted(changes, key=lambda c: int(c['timestamp']))

    def __watch(self):
        with self.submissions.watch() as stream:
            for change in stream:
                self.__process(change)
