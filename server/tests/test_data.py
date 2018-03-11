class AberUndergrad:
    FULL_NAME = 'John Smith'
    CAMPUS = 'AB'
    CARD_TYPE = 'AU'
    USER_TYPE = CAMPUS + CARD_TYPE
    GECOS = '{},ADN,,,[{}]'.format(FULL_NAME, USER_TYPE)
    UID = 'jos1'
    PASSWORD = 'abc123'


class AberStaff:
    FULL_NAME = 'Mike Jones'
    CAMPUS = 'AB'
    CARD_TYPE = 'SM'
    USER_TYPE = CAMPUS + CARD_TYPE
    GECOS = '{},ADN,,,[{}]'.format(FULL_NAME, USER_TYPE)
    UID = 'mij22'
    PASSWORD = 'itsmike'
