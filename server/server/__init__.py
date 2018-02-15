import logging
import os

from .web import start

log = logging.getLogger(__name__)


def _real_main():
    debug = os.environ['PDS_DEBUG']

    setup_logging(debug)

    start(debug)


def main():
    try:
        _real_main()
    except KeyboardInterrupt:
        pass


def setup_logging(debug):
    log_level = logging.INFO

    if debug:
        log_level = logging.DEBUG

    logging.basicConfig(format='%(levelname)-8s %(asctime)s: %(name)20s '
                               '[%(filename)20s:%(lineno)-4s %(funcName)-20s] '
                               '%(message)s', level=log_level)
