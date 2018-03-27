import logging


class FileProcessor:
    def __init__(self, path, data) -> None:
        super().__init__()
        self.log = logging.getLogger(type(self).__name__)
        self.path = path
        self.cache = data['cache']
        self.changes = data['changes']
        self.path = data['path']

    def __build_document(self):
        document = ''

        # Ensure changes are sorted by timestamp
        sorted_changes = sorted(self.changes,
                                key=lambda ch: int(ch['timestamp']))

        for c in sorted_changes:
            # get change data
            old_str = c['oldString']
            new_str = c['newString']
            offset = int(c['offset'])

            start = document[:offset] if len(document) > 0 else ''
            end = document[offset + len(old_str):] if len(document) > 0 else ''

            document = start + new_str + end

        return document

    def process(self):
        self.log.info('Processing file: {}'.format(self.path))

        document = self.__build_document()

        self.log.info(document)
