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

    submit(args.uid, args.title, args.module, args.file)


def do_auth(uid):
    password = getpass.getpass()
    return ldap.auth(uid, password)


def do_parse_xml(filename):
    data = xml_parser.parse(filename)
    log.debug('Parsed XML: %s', json.dumps(data))
    return data


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--uid', help='User id for authorisation',
                        required=True)
    parser.add_argument('-t', '--title', help='The submission title',
                        required=True)
    parser.add_argument('-m', '--module', help='The submission module',
                        required=True)
    parser.add_argument('-f', '--file', help='The submission file')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enable debug logging')
    return parser.parse_args()


def setup_logging(debug):
    log_level = logging.INFO

    if debug:
        log_level = logging.DEBUG

    logging.basicConfig(format='%(levelname)-8s %(asctime)s: %(name)20s '
                               '[%(filename)20s:%(lineno)-4s %(funcName)-20s] '
                               '%(message)s', level=log_level)


def submit(uid, title, module, filename, processed=False):
    if not do_auth(uid):
        return

    xml_data = do_parse_xml(filename)

    submissions = db.SubmissionCollection(db.get_plagiarism_db())

    submissions.insert_one(uid, title, module, xml_data, processed)


if __name__ == '__main__':
    main()
