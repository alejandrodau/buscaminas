import requests


class BuscaminasClientException(Exception):
    pass


class BuscaminasClient():
    """ Minesweeper client class """
    def __init__(self, url="http://buscaminas.hopto.org:5555/"):
        self._url = url
        self._sessionToken = None

    def _validResponse(self, req):
        if req.status_code == 400:
            raise BuscaminasClientException(req.json()['error']['errorCode'])
        req.raise_for_status()
        return True

    def addUser(self, user, passwd):
        r = requests.post(self._url + '/user/add', data={'user': user, 'passwd': passwd})
        if self._validResponse(r):
            self._sessionToken = r.json()['token']

    def login(self, user, passwd):
        r = requests.post(self._url + '/user/login', data={'user': user, 'passwd': passwd})
        if self._validResponse(r):
            self._sessionToken = r.json()['token']

    def getBoard(self, gameId):
        r = requests.get(self._url + '/board/' + gameId, headers={'Authorization': self._sessionToken})
        if self._validResponse(r):
            return r.json()

    def newGame(self, xsize, ysize, mines):
        r = requests.post(self._url + '/newGame',
                          headers={'Authorization': self._sessionToken},
                          data={'xsize': xsize, 'ysize': ysize, 'mines': mines})
        if self._validResponse(r):
            return r.json()['gameId']

    def uncover(self, gameId, x, y):
        r = requests.put(self._url + '/board/' + gameId + '/uncover',
                          headers={'Authorization': self._sessionToken},
                          data={'x': x, 'y': y})
        if self._validResponse(r):
            return r.json()

    def flag(self, gameId, x, y):
        r = requests.put(self._url + '/board/' + gameId + '/flag',
                          headers={'Authorization': self._sessionToken},
                          data={'x': x, 'y': y})
        if self._validResponse(r):
            return r.json()

'''
# TODO. Implement client methods for:
* remove flag
* add/remove question marks
* logout
* gameList
* Improve error handling
* Remove redundance in url construction and response validation
'''
