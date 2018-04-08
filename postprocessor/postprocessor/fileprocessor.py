import logging
from difflib import SequenceMatcher


class FileProcessor:
    """
    The FileProcessor is used to process each file in a submission
    and give a result
    """

    def __init__(self, cache, changes, plot=False) -> None:
        """
        Create a new FileProcessor
        :param cache: The cache of the file contents
        :param changes: The list of changes
        :param plot: true to plot using matplotlib; false otherwise
        """
        super().__init__()
        self.log = logging.getLogger(type(self).__name__)
        self.cache = cache
        self.changes = changes
        self.plot = plot

    def __build_frequency_time_source_data(self):
        """
        Build data for frequency vs. time (with source labels) plot
        :return: List of rows for plotting
        """
        rows = []

        # Add each change as a new row
        for c in self.changes:
            add = len(c['newString'])
            rem = len(c['oldString'])
            # Normalise the difference in change
            diff = add - rem

            rows.append({
                'f': diff,
                's': c['source'],
                't': int(c['timestamp'])
            })

        return rows

    def __build_document(self):
        """
        Reconstruct the file from the list of changes
        :return: The final file document
        """
        document = ''

        # Add each change to the document
        for c in self.changes:
            # Get change data
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
        """
        Get the frequency for a given source (or all if None)
        :param source: The source to get the frequency of
        :return: The frequency of the source
        """
        total = 0

        # Get frequency over all changes
        for c in self.changes:
            if source is None or c['source'] == source:
                total += len(c['newString']) - len(c['oldString'])

        return total

    def __get_diff_ratio(self):
        """
        Get the difference ratio between the cache and reconstructed document
        :return: The difference ratio
        """
        # Reconstruct the document from the list of changes
        built = self.__build_document()
        # Get the diff ratio between the cache and reconstructed document
        return SequenceMatcher(None, self.cache, built).ratio()

    def process(self):
        """
        Process the file data and return the result
        :return: A dictionary of metrics
        """
        fts_data = self.__build_frequency_time_source_data()
        total_f = self.__build_frequency()
        clipboard_f = self.__build_frequency('CLIPBOARD')
        external_f = self.__build_frequency('EXTERNAL')
        other_f = self.__build_frequency('OTHER')
        diff_ratio = self.__get_diff_ratio()

        return {
            'diff_ratio': diff_ratio,
            'frequency_total': total_f,
            'frequency_clipboard': clipboard_f,
            'frequency_external': external_f,
            'frequency_other': other_f,
            'frequency_time_source_data': fts_data,
        }
