import base64
import logging
import os
from textwrap import wrap

import matplotlib.pyplot as plt
from mockupdb import MockupDB

from postprocessor.db import SubmissionCollection
from postprocessor.fileprocessor import FileProcessor
from postprocessor.xml_parser import cipherparse

# Matplotlib source colors
_SOURCES = {'CLIPBOARD': 'r', 'EXTERNAL': 'b', 'OTHER': 'k'}


class PostProcessor:
    """
    The PostProcessor will process submissions
    """

    def __init__(self, plot=False) -> None:
        """
        Create a new PostProcessor and plot using matplotlib
        :param plot: true to plot using matplotlib; false otherwise
        """
        super().__init__()
        self.log = logging.getLogger(type(self).__name__)
        self.plot = plot
        # Submissions collection for the plagiarism database
        self.submissions = SubmissionCollection()

    def mockdb(self):
        """
        Mock the plagiarism db and submissions collection
        :return: The MockupDB instance
        """
        mockdb = MockupDB(auto_ismaster=True)
        mockdb.run()
        self.submissions = SubmissionCollection(uri=mockdb.uri)
        return mockdb

    def __plot_frequency_time_source(self, fts_data):
        """
        Plot frequency vs. time (and source colors) using matplotlib
        :param fts_data: The data to plot
        """
        if self.plot:
            initial_t = fts_data[0]['t']
            # Normalise timestamps
            for r in fts_data:
                r['t'] -= initial_t

            # Plot each source as a scatter plot using its color
            for s, c in _SOURCES.items():
                x = [r['t'] for r in fts_data if r['s'] == s]
                y = [r['f'] for r in fts_data if r['s'] == s]
                plt.scatter(x, y, c=c, s=2, zorder=2, label=s)

            # Plot all data as a line
            x = [r['t'] for r in fts_data]
            y = [r['f'] for r in fts_data]

            plt.plot(x, y, linewidth=1, color='k', zorder=1)

            # Show legend for scatter plots
            plt.legend()
            plt.title('\n'.join(
                wrap('Character Frequency vs. Time')))
            plt.xlabel('Time (ms)')
            plt.ylabel('Frequency')
            plt.show()

    def __process(self, submission):
        """
        Process a submission
        :param submission: The submission to process
        :return: The processed result
        """
        self.log.info('Processing submission...')

        results = {}

        # Process each file in the submission
        for path, data in submission.items():
            # Ensure changes are sorted by timestamp
            changes = sorted(data['changes'], key=lambda c: int(c['timestamp']))
            # Decode the document cache
            cache = base64.b64decode(data['cache']).decode('utf-8')
            results[path] = FileProcessor(cache, changes, self.plot).process()

        merged_fts_data = []

        # Merge all fts data from each file to make one data set
        for p, result in results.items():
            merged_fts_data += result['frequency_time_source_data']

        # Sort fts data by time
        merged_fts_data = sorted(merged_fts_data, key=lambda d: int(d['t']))

        # Use matplotlib to plot merged fts graph
        self.__plot_frequency_time_source(merged_fts_data)

        self.log.debug('Results: {}'.format(results))

        return results

    def __process_change(self, change):
        """
        Process a change in the database
        This will process new submissions and add the processed result to the
        database
        :param change: The database change
        """
        # Get the changed document id
        _id = change['documentKey']['_id']
        # Only watch for updates to a users submission
        if 'updateDescription' not in change:
            return

        upd_desc = change['updateDescription']
        if 'updatedFields' not in upd_desc:
            return

        for key, value in upd_desc['updatedFields'].items():
            # Look for valid submissions
            # First submission will add the submission list
            if key == 'submissions':
                for submission in value:
                    self.__process_submission(_id, submission)
            elif 'files' in value:
                self.__process_submission(_id, value)

    def __process_submission(self, _id, submission):
        """
        Process a submission and update the database with the result
        :param _id: The document id
        :param submission: The submission to process
        :return: The result from updating the submission in the databse
        """
        # Process the submission
        result = self.__process(submission['files'])
        # Update the database with the result
        return self.submissions.update_submission(_id, submission, result)

    def run(self, filename=None):
        """
        Set up logging and start the post processor
        :param filename the filename of the submission to process; if None
        will watch the submissions collection in the plagiarism database
        """
        # Set PDP_DEBUG in the environment to enable debug
        # Use env instead of args because we are using Docker
        debug = 'PDP_DEBUG' in os.environ

        self.setup_logging(debug)

        if filename is None:
            self.__watch()
        else:
            return self.__process(cipherparse(filename))

    @staticmethod
    def setup_logging(debug):
        """
        Configure logging with a custom format and debug logging
        :param debug: Set to True to enable debug logging
        """
        log_level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(format='%(levelname)-8s %(asctime)s: %(name)20s '
                                   '[%(filename)20s:%(lineno)-4s '
                                   '%(funcName)-20s] %(message)s',
                            level=log_level)

    def __watch(self):
        # Watch the stream for changes
        with self.submissions.watch() as stream:
            for change in stream:
                self.__process_change(change)
