import logging

from pymongo import MongoClient

# MongoDB options
MONGODB_HOST = 'mongodb'
MONGODB_PORT = 27017

DB_PLAGIARISM = 'plagiarism'

log = logging.getLogger(__name__)


def get_client():
    """
    Get the MongoDB client
    :return: A MongoClient
    """
    return MongoClient(MONGODB_HOST, MONGODB_PORT)


def get_plagiarism_db():
    """
    Get the plagiarism database
    :return: The plagiarism Database
    """
    return get_client()[DB_PLAGIARISM]


class SubmissionCollection:
    """
    A wrapper for the submissions collection
    """

    # The collection name
    NAME = 'submissions'

    def __init__(self, db) -> None:
        """
        Create a new SubmissionCollection within a given database
        :param db: The database which contains the collection
        """
        super().__init__()
        self.log = logging.getLogger(type(self).__name__)
        self.submissions = db[SubmissionCollection.NAME]

    @staticmethod
    def __convert_keys(data):
        """
        Convert $ (dollar sign) and . (dot) in the keys to __
        (double underscore)
        :param data: The data to convert the keys
        :return: The data with the converted keys
        """
        converted = {}
        for key in data.keys():
            converted[key.replace('$', '__').replace('.', '__')] = data[key]
        return converted

    def find(self, *args, **kwargs):
        """
        Query a submission. See pymongo.collection.find()
        """
        self.log.debug('Find submission: %s, %s', args, kwargs)
        return self.submissions.find(*args, **kwargs)

    def find_by_module(self, module):
        """
        Finds all user submissions for the given module
        :param module: The module to filter by
        :return: All user submissions for the module
        """
        self.log.debug('Aggregate module: %s', module)
        return self.submissions.aggregate([
            {
                '$match': {
                    'submissions.module': module
                },
            },
            {
                '$project': {
                    'submissions': {
                        '$filter': {
                            'input': '$submissions',
                            'as': 'submission',
                            'cond': {
                                '$eq': [
                                    '$$submission.module', module
                                ]
                            }
                        }
                    }
                }
            }
        ])

    def find_user(self, uid):
        """
        Find a users' submissions by uid
        :param uid: The user id
        :return: The users' submissions
        """
        self.log.debug('Find user: %s', uid)
        return self.submissions.find_one({'uid': uid})

    def insert_one(self, uid, title, module, files=None, processed=False):
        """
        Add a new submission for a user
        :param uid: The user id
        :param title: The submission title
        :param module: The submission module
        :param files: The submission file data
        :param processed: True if the data has been processed; False otherwise
        :return: An instance of :class:`~pymongo.results.InsertOneResult` or
        :class:`~pymongo.results.UpdateResult` depending if the user has
        existing submissions
        """
        if files is None:
            files = {}

        uid_filter = {
            'uid': uid
        }
        data = {
            '$push': {
                'submissions': {
                    'title': title,
                    'module': module,
                    # Must convert keys for file data incase of $ of . in keys
                    'files': SubmissionCollection.__convert_keys(files),
                    'processed': processed
                }
            }
        }

        self.log.debug(
            'Insert submission: uid={}, submission={}'.format(uid, data))

        res = self.submissions.update_one(uid_filter, data)
        log.debug('Submission result: matched=%s, modified=%s',
                  res.matched_count, res.modified_count)
        return res

    def insert_user(self, user):
        # Find the user submissions, if any
        stored_user = self.submissions.find_one({'uid': user.uid})
        uid_filter = {
            'uid': user.uid
        }
        user_data = {
            'uid': user.uid,
            'full_name': user.full_name,
            'user_type': user.user_type,
            'submissions': []
        }

        self.log.debug('Insert user: uid=%s', user)

        if stored_user is None:
            res = self.submissions.insert_one(user_data)
            log.debug('Submission result: id=%s', res.inserted_id)
            return res
        else:
            res = self.submissions.update_one(uid_filter, user_data)
            log.debug('Submission result: matched=%s, modified=%s',
                      res.matched_count, res.modified_count)
            return res
