import getpass
import json
import logging

from .db import SubmissionCollection, get_plagiarism_db
from .ldap import auth
from .xml_parser import parse


class Submission:
    def __init__(self, uid, title, module, filename, processed=False) -> None:
        super().__init__()
        self.log = logging.getLogger(type(self).__name__)
        self.uid = uid
        self.title = title
        self.module = module
        self.filename = filename
        self.processed = processed

    def __auth(self):
        password = getpass.getpass()
        return auth(self.uid, password)

    def __parse_xml(self):
        data = parse(self.filename)
        self.log.debug('Parsed XML: %s', json.dumps(data))
        return data

    def submit(self):
        if not self.__auth():
            return

        xml_data = self.__parse_xml()

        submissions = SubmissionCollection(get_plagiarism_db())

        submissions.insert_one(self.uid, self.title, self.module, xml_data,
                               self.processed)
