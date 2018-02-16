CARD_TYPE_STAFF = 'SM'


class User:
    """
    This class is used to represent a user
    See: https://flask-login.readthedocs.io/en/latest/#your-user-class
    """

    def __init__(self, uid, full_name, user_type):
        self.uid = uid
        self.full_name = full_name
        self.user_type = user_type

    def get_card_type(self):
        return self.user_type[2:]

    def get_id(self):
        return self.uid

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def is_staff(self):
        return self.get_card_type() == CARD_TYPE_STAFF

    def __str__(self) -> str:
        return 'User{{uid={},full_name={},user_type={}}}'.format(self.uid,
                                                                 self.full_name,
                                                                 self.user_type)
