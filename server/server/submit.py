import json
import logging

from server import submissions
from server.xml_parser import parse


class Submission:
    """
    This class is used to submit a new submission for a user
    """

    def __init__(self, uid, title, module, filename, processed=False) -> None:
        super().__init__()
        self.log = logging.getLogger(type(self).__name__)
        self.uid = uid
        self.title = title
        self.module = module
        self.filename = filename
        self.processed = processed

    def __parse_xml(self):
        """
        Parse the XML file
        :return: The parsed XML data
        """
        data = parse(self.filename)
        self.log.debug('Parsed XML: %s', json.dumps(data))
        return data

    def submit(self):
        """
        Submit the submission into the database
        """
        submissions.insert_one(self.uid, self.title, self.module,
                               self.__parse_xml(), self.processed)
