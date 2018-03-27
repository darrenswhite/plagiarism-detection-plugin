import logging

from pymongo import MongoClient

log = logging.getLogger(__name__)

# MongoDB options
MONGODB_URI = 'mongodb://mongodb:27017/'
DB_PLAGIARISM = 'plagiarism'
COLL_SUBMISSIONS = 'submissions'


class SubmissionCollection:
    """
    A wrapper for the submissions collection
    """

    def __init__(self, uri=MONGODB_URI) -> None:
        """
        Create a new SubmissionCollection within a given database
        :param uri: The MongoDB connection uri
        """
        super().__init__()
        self.log = logging.getLogger(type(self).__name__)
        self.client = MongoClient(uri)
        self.database = self.client[DB_PLAGIARISM]
        self.submissions = self.database[COLL_SUBMISSIONS]

    def watch(self):
        if COLL_SUBMISSIONS not in self.database.list_collection_names():
            self.log.info('Creating {} collection'.format(COLL_SUBMISSIONS))
            self.database.create_collection(COLL_SUBMISSIONS)

        self.log.info('Watching submission collection')
        return self.submissions.__watch()
