import logging
from textwrap import wrap

import matplotlib.pyplot as plt

_SOURCES = {'CLIPBOARD': 'r', 'EXTERNAL': 'b', 'OTHER': 'k'}


class ChangeProcessor:
    def __init__(self, changes, plot=False) -> None:
        super().__init__()
        self.log = logging.getLogger(type(self).__name__)
        self.changes = changes
        self.plot = plot

    def __build_character_frequency_time_data(self):
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

    def __build_frequency(self, source=None):
        total = 0

        for c in self.changes:
            if source is None or c['source'] == source:
                total += len(c['newString']) - len(c['oldString'])

        return total

    def __plot(self):
        f_graph = self.__build_character_frequency_time_data()

        for s, c in _SOURCES.items():
            x = [r['t'] for r in f_graph if r['s'] == s]
            y = [r['f'] for r in f_graph if r['s'] == s]
            plt.scatter(x, y, c=c, s=2, zorder=2, label=s)

        x = [r['t'] for r in f_graph]
        y = [r['f'] for r in f_graph]
        plt.plot(x, y, linewidth=1, color='k', zorder=1)

        plt.legend()
        plt.title('\n'.join(
            wrap('Character Frequency vs. Time')))
        plt.xlabel('Time (ms)')
        plt.ylabel('Frequency')
        plt.show()

    def process(self):
        if self.plot:
            self.__plot()

        total_f = self.__build_frequency()
        clipboard_f = self.__build_frequency('CLIPBOARD')
        external_f = self.__build_frequency('EXTERNAL')

        return {
            'frequency_total': total_f,
            'frequency_clipboard': clipboard_f,
            'frequency_external': external_f
        }
