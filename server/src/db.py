import logging

from pymongo import MongoClient

log = logging.getLogger(__name__)


def test():
    client = MongoClient('mongodb://localhost:27017')
    db = client.plagiarism
    db.command("dropDatabase")
    submissions = SubmissionCollection(db)

    submissions.insert_one('daw48', 'My Submission', 'CS404040')

    daw48_submissions = submissions.find({'uid': 'daw48'})

    log.info('daw48 submissions:')
    for s in daw48_submissions:
        log.info(s)

    submissions.insert_one('dab14', 'Test Submission', 'CS404040',
                           processed=True)
    submissions.insert_one('daw48', 'My 2nd Submission', 'CS505050')

    daw48_submissions = submissions.find({'uid': 'daw48'})

    log.info('daw48 submissions:')
    for s in daw48_submissions:
        log.info(s)

    cs505050_submissions = submissions.find_by_module('CS505050')

    log.info('CS505050 submissions:')
    for s in cs505050_submissions:
        log.info(s)


class SubmissionCollection:
    NAME = 'submissions'

    def __init__(self, client) -> None:
        super().__init__()
        self.log = logging.getLogger(type(self).__name__)
        self.db = client[SubmissionCollection.NAME]

    def find(self, *args, **kwargs):
        self.log.debug('Find submission: %s, %s', args, kwargs)
        return self.db.find(*args, **kwargs)

    def find_by_module(self, module):
        self.log.debug('Aggregate module: %s', module)
        return self.db.aggregate([
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

    def insert_one(self, uid, title, module, files=None, processed=False):
        if files is None:
            files = {}

        user = self.db.find_one({'uid': uid})
        submission = {
            'title': title,
            'module': module,
            'files': convert_keys(files),
            'processed': processed
        }

        self.log.debug(
            'Insert submission: uid={}, submission={}'.format(uid, submission))

        if user is None:
            self.log.debug('Inserting a new submission')
            data = {
                'uid': uid,
                'submissions': [submission]
            }
            res = self.db.insert_one(data)
            log.debug('Submission result: id=%s', res.inserted_id)
            return res
        else:
            self.log.debug('Updating submission')
            uid_filter = {
                'uid': uid
            }
            data = {
                '$push': {
                    'submissions': submission
                }
            }
            res = self.db.update_one(uid_filter, data)
            log.debug('Submission result: matched=%s, modified=%s',
                      res.matched_count, res.modified_count)
            return res


def convert_keys(data):
    converted = {}
    for key in data.keys():
        converted[key.replace('$', '__').replace('.', '__')] = data[key]
    return converted
