import uuid
import hashlib


class UserDB():
    # TODO. This is a mock implementation. Implement this in a proper DB
    # including athentication and token expiration

    def __init__(self):
        self._userData = {}
        self._tokenToUser = {}

    def addUser(self, user, passwd):
        ''' Add a user to the database '''
        if user in self._userData:
            raise UserAlreadyExists
        userToken = self._getNewToken(user)
        hashedPasswd = self._getHashedPassword(passwd)
        self._userData[user] = {'passwd': hashedPasswd, 'games': []}
        return userToken

    def _getHashedPassword(self, passwd):
        return hashlib.sha224(bytes('NaCl' + passwd, 'utf-8')).hexdigest()

    def _getNewToken(self, user):
        userToken = str(uuid.uuid4())
        self._tokenToUser[userToken] = user
        return userToken

    def login(self, user, passwd):
        ''' login and return token '''
        try:
            if self._userData[user]['passwd'] == \
               self._getHashedPassword(passwd):
                return self._getNewToken(user)
        except KeyError:
            pass
        raise BadUserOrPass()

    def logout(self, token):
        ''' remove session token '''
        try:
            del self._tokenToUser[token]
        except KeyError:
            # no worries if token already does not exist
            pass

    def addGameId(self, token, gameId):
        ''' add game Id to the game list of the user '''
        # TODO: handle wrong session
        userData = self._userData[self._tokenToUser[token]]
        userData['games'].append(gameId)

    def getGameList(self, token):
        ''' get game Id list for the current user '''
        # TODO: handle wrong session
        userData = self._userData[self._tokenToUser[token]]
        return userData['games']


class BadUserOrPass(Exception):
    pass


class UserAlreadyExists(Exception):
    pass
