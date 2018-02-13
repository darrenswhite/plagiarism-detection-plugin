import logging

from ldap3 import Connection, Server
from ldap3.core.exceptions import LDAPBindError

LDAP_PORT = 636
LDAP_SERVER = 'ldap.dcs.aber.ac.uk'

log = logging.getLogger(__name__)


def main():
    setup_logging()

    server = ldap_server()

    try:
        with ldap_connection(server, 'daw48', 'password') as conn:
            if conn.bind():
                log.info('Authentication successful')
                log.debug(conn)
                log.debug(conn.extend.standard.who_am_i())
            else:
                log.info('Authentication failed')
    except LDAPBindError as e:
        log.error(e)


def ldap_server():
    return Server(LDAP_SERVER, port=LDAP_PORT, use_ssl=True)


def ldap_connection(server, uid, password):
    return Connection(server,
                      'uid=%s,ou=People,dc=dcs,dc=aber,dc=ac,dc=uk'.format(uid),
                      password)


def setup_logging():
    logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    main()
