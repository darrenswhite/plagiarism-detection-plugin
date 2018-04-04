import logging

from ldap3 import Connection, Server
from ldap3.core.exceptions import LDAPException

from server.auth.user import User

LDAP_PORT = 636
LDAP_SERVER = 'ldap.dcs.aber.ac.uk'

GECOS_FULL_NAME = 0
GECOS_USER_TYPE = 4

USER_FORMAT = 'uid={},ou=People,dc=dcs,dc=aber,dc=ac,dc=uk'

log = logging.getLogger(__name__)


def try_bind(uid, password):
    """
    Try and login a user given a uid and password
    :param uid: The user id to login with
    :param password: The password to login with
    :return: User if successful; None otherwise
    """
    log.info('Attempting authentication for: %s', uid)

    try:
        with connection(uid, password) as conn:
            # Try and authenticate the user
            if conn.bind():
                log.info('Authentication successful')
                log.debug('Connection: %s', conn)
                log.debug('whoami: %s', conn.extend.standard.who_am_i())
                # Lookup their details
                if conn.search('dc=dcs,dc=aber,dc=ac,dc=uk',
                               '(uid={})'.format(uid), attributes=['gecos']):
                    gecos = conn.entries[0]['gecos'].value
                    gecos_parts = gecos.split(',')
                    log.debug('gecos: %s', gecos_parts)
                    # gecos contains full name and user type
                    full_name = gecos_parts[GECOS_FULL_NAME]
                    user_type = gecos_parts[GECOS_USER_TYPE] \
                        .replace('[', '').replace(']', '')
                    return User(uid, full_name, user_type)
            else:
                log.warning('Authentication failed: failed to bind connection')
                return None
    except LDAPException as e:
        log.error('Authentication failed: %s', e)
        return None


def connection(uid, password):
    """
    Get the LDAP connection
    :param uid: The user id
    :param password: The user password
    :return: An LDAP Connection
    """
    return Connection(server(), USER_FORMAT.format(uid), password)


def server():
    """
    Get the LDAP server
    :return: An LDAP Server
    """
    return Server(LDAP_SERVER, port=LDAP_PORT, use_ssl=True)
