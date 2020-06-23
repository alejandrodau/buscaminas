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
