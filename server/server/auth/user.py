from server.ldap import auth


class User:
    """
    This class is used to represent a user
    See: https://flask-login.readthedocs.io/en/latest/#your-user-class
    """

    def __init__(self, uid):
        self.uid = uid

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.uid

    @staticmethod
    def try_login(uid, password):
        """
        Try and login the user given a uid and password using LDAP
        :param uid: The uid to login with
        :param password: The password to login with
        :return: True if login was successful; False otherwise
        """
        return auth(uid, password)
