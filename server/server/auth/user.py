CARD_TYPE_STAFF = 'SM'


class User:
    """
    This class is used to represent a user
    See: https://flask-login.readthedocs.io/en/latest/#your-user-class
    """

    def __init__(self, uid, full_name, user_type):
        """
        Create a new User with the uid, fullname, and type
        :param uid: Unique ID for the user
        :param full_name: Full name for the user
        :param user_type: Type of user; SM for Staff, UG for undergraduate
        """
        self.uid = uid
        self.full_name = full_name
        self.user_type = user_type

    def get_card_type(self):
        """
        The User card type
        :return:
        """
        # User type contains the card type
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
        """
        Checks if this User is staff
        :return: true if the user is staff; false otherwise
        """
        return self.get_card_type() == CARD_TYPE_STAFF

    def __str__(self) -> str:
        return 'User{{uid={},full_name={},user_type={}}}'.format(self.uid,
                                                                 self.full_name,
                                                                 self.user_type)
