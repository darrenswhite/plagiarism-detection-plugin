class User:
    """
    This class is used to represent a user
    See: https://flask-login.readthedocs.io/en/latest/#your-user-class
    """

    def __init__(self, uid, full_name, user_type):
        self.uid = uid
        self.full_name = full_name
        self.user_type = user_type

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.uid
