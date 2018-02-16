import logging

from ldap3 import Connection, Server
from ldap3.core.exceptions import LDAPException

LDAP_PORT = 636
LDAP_SERVER = 'ldap.dcs.aber.ac.uk'

log = logging.getLogger(__name__)


def auth(uid, password):
    """
    Try and authentication a user given a uid and password
    :param uid: The user id to login with
    :param password: The password to login with
    :return: True if successful; False otherwise
    """
    log.info('Attempting authentication for: %s', uid)

    server = ldap_server()

    try:
        with ldap_connection(server, uid, password) as conn:
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
    """
    Get the LDAP connection
    :param server: The LDAP server
    :param uid: The user id
    :param password: The user password
    :return: An LDAP Connection
    """
    return Connection(server,
                      'uid={},ou=People,dc=dcs,dc=aber,dc=ac,dc=uk'.format(uid),
                      password)


def ldap_server():
    """
    Get the LDAP server
    :return: An LDAP Server
    """
    return Server(LDAP_SERVER, port=LDAP_PORT, use_ssl=True)
