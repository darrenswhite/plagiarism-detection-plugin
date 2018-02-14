import logging

from ldap3 import Connection, Server
from ldap3.core.exceptions import LDAPException

LDAP_PORT = 636
LDAP_SERVER = 'ldap.dcs.aber.ac.uk'

log = logging.getLogger(__name__)


def auth(user, password):
    log.info('Attempting authentication for %s', user)

    server = ldap_server()

    try:
        with ldap_connection(server, user, password) as conn:
            if conn.bind():
                log.info('Authentication successful')
                log.debug('Connection: %s', conn)
                log.debug('whoami: %s', conn.extend.standard.who_am_i())
                return True
            else:
                log.warning('Authentication failed: failed to bind connection')
                return False
    except LDAPException as e:
        log.error('Authentication failed: %s', e)
        return False


def ldap_connection(server, uid, password):
    return Connection(server,
                      'uid={},ou=People,dc=dcs,dc=aber,dc=ac,dc=uk'.format(uid),
                      password)


def ldap_server():
    return Server(LDAP_SERVER, port=LDAP_PORT, use_ssl=True)
