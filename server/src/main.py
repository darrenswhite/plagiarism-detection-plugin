#!/usr/bin/python3

import argparse
import getpass
import json
import logging

import db
import ldap
import xml_parser

log = logging.getLogger(__name__)


def main():
    args = parse_args()

    setup_logging(args.debug)

    log.debug('args: %s', args)

    if args.command == 'auth':
        do_auth()
    elif args.command == 'db':
        do_db()
    elif args.command == 'xml':
        do_xml(args.filename)


def do_auth():
    user = input('User: ')
    password = getpass.getpass()
    ldap.auth(user, password)


def do_db():
    db.test()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--command', help='Command to run', required=True)
    parser.add_argument('-f', '--filename', help='Filename for XML')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enable debug logging')
    return parser.parse_args()


def do_xml(filename):
    data = xml_parser.parse(filename)
    log.debug('Parsed XML: %s', json.dumps(data))


def setup_logging(debug):
    log_level = logging.INFO

    if debug:
        log_level = logging.DEBUG

    logging.basicConfig(format='%(levelname)-8s %(asctime)s: %(name)20s '
                               '[%(filename)20s:%(lineno)-4s %(funcName)-20s] '
                               '%(message)s', level=log_level)


if __name__ == '__main__':
    main()
