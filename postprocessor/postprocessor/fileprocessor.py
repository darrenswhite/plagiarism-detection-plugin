import logging
from difflib import SequenceMatcher


class FileProcessor:
    def __init__(self, cache, changes, plot=False) -> None:
        super().__init__()
        self.log = logging.getLogger(type(self).__name__)
        self.cache = cache
        self.changes = changes
        self.plot = plot

    def __build_frequency_time_source_data(self):
        rows = []
        initial_t = int(self.changes[0]['timestamp']) if len(
            self.changes) > 0 else 0

        for c in self.changes:
            add = len(c['newString'])
            rem = len(c['oldString'])
            diff = add - rem

            rows.append({
                'f': diff,
                's': c['source'],
                't': int(c['timestamp']) - initial_t
            })

        return rows

    def __build_document(self):
        document = ''

        for c in self.changes:
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

    def __build_frequency(self, source=None):
        total = 0

        for c in self.changes:
            if source is None or c['source'] == source:
                total += len(c['newString']) - len(c['oldString'])

        return total

    def __get_diff_ratio(self):
        # Reconstruct the document from the list of changes
        built = self.__build_document()
        # Get the diff ratio between the cache and reconstructed document
        return SequenceMatcher(None, self.cache, built).ratio()

    def process(self):
        fts_data = self.__build_frequency_time_source_data()
        total_f = self.__build_frequency()
        clipboard_f = self.__build_frequency('CLIPBOARD')
        external_f = self.__build_frequency('EXTERNAL')
        diff_ratio = self.__get_diff_ratio()

        return {
            'diff_ratio': diff_ratio,
            'frequency_total': total_f,
            'frequency_clipboard': clipboard_f,
            'frequency_external': external_f,
            'frequency_time_source_data': fts_data,
        }
