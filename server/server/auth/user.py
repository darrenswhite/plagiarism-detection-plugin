from server.ldap import auth


class User:
    def __init__(self, username):
        self.uid = username

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
        return auth(uid, password)
