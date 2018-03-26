class AberUndergrad:
    FULL_NAME = 'John Smith'
    CAMPUS = 'AB'
    CARD_TYPE = 'AU'
    USER_TYPE = CAMPUS + CARD_TYPE
    GECOS = '{},ADN,,,[{}]'.format(FULL_NAME, USER_TYPE)
    UID = 'jos1'
    PASSWORD = 'abc123'
    SUBMISSIONS = [
        {
            'title': 'Test Submission A',
            'module': 'Test Module',
            'files': {}
        },
        {
            'title': 'Test Submission B',
            'module': 'Test Module',
            'files': {}
        }
    ]


class AberUndergrad2:
    FULL_NAME = 'Jake Deck'
    CAMPUS = 'AB'
    CARD_TYPE = 'AU'
    USER_TYPE = CAMPUS + CARD_TYPE
    GECOS = '{},ADN,,,[{}]'.format(FULL_NAME, USER_TYPE)
    UID = 'jad24'
    PASSWORD = 'jakedeck$$$'
    SUBMISSIONS = [
        {
            'title': 'Jake Deck 1',
            'module': 'My Module',
            'files': {}
        },
        {
            'title': 'Jake Deck 2',
            'module': 'Another Module',
            'files': {}
        }
    ]


class AberStaff:
    FULL_NAME = 'Mike Jones'
    CAMPUS = 'AB'
    CARD_TYPE = 'SM'
    USER_TYPE = CAMPUS + CARD_TYPE
    GECOS = '{},ADN,,,[{}]'.format(FULL_NAME, USER_TYPE)
    UID = 'mij22'
    PASSWORD = 'itsmike'
