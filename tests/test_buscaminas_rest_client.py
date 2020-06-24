
import pytest
import itertools
import responses
import json

from buscaminas_rest_client import BuscaminasClient, BuscaminasClientException


mockUrl = 'http://testserver:5000'
token = "633e6e3f-43c1-428b-9660-38fe3bb6035c"
gameId = "75fd6be1-5320-4677-8106-1c71f09af6f1"

# TODO: *********** Test unhappy paths! ***************

@pytest.fixture
def client():
    return BuscaminasClient(mockUrl)


@responses.activate
def test_addUser(client):
    expectedToken = token
    responses.add(responses.POST, mockUrl + '/user/add',
                  json={'token': expectedToken}, status=200)

    client.addUser('pepe', 'pepepass')
    assert client._sessionToken == expectedToken


def _doLogin(client):
    responses.add(responses.POST, mockUrl + '/user/login',
                  json={'token': token}, status=200)
    client.login('pepe', 'pepepass')


@responses.activate
def test_login(client):
    _doLogin(client)
    assert client._sessionToken == token


@responses.activate
def test_badLogin(client):
    responses.add(responses.POST, mockUrl + '/user/login',
                  json={'error': {'errorCode': 'BadUserOrPass'}}, status=400)

    with pytest.raises(BuscaminasClientException):
        client.login('pepe', 'pepepass')


@responses.activate
def test_getBoard(client):
    gameId = "75fd6be1-5320-4677-8106-1c71f09af6f1"
    board = json.loads('{"board":[[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."]],"status":"active"}')

    responses.add(responses.GET, mockUrl + '/board/' + gameId, headers={'Authorization': token},
                  json=board, status=200)

    _doLogin(client)
    assert client.getBoard(gameId) == board


def _createNewGame(client):
    board = json.loads('{"board":[[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."]],"status":"active"}')
    responses.add(responses.POST, mockUrl + '/newGame', headers={'Authorization': token},
                  json={'gameId': gameId}, status=200)
    return client.newGame(5, 5, 3)


@responses.activate
def test_newGame(client):
    _doLogin(client)
    assert _createNewGame(client) == gameId


@responses.activate
def test_uncover(client):
    _doLogin(client)
    gameId = _createNewGame(client)

    board = json.loads('{"board":[["1",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."]],"status":"active"}')
    responses.add(responses.PUT, mockUrl + '/board/' + gameId + '/uncover',
                  headers={'Authorization': token}, json=board, status=200)

    assert client.uncover(gameId, 0, 0) == board


@responses.activate
def test_flag(client):
    _doLogin(client)
    gameId = _createNewGame(client)


    board = json.loads('{"board":[["F",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."]],"status":"active"}')
    responses.add(responses.PUT, mockUrl + '/board/' + gameId + '/flag',
                  headers={'Authorization': token}, json=board, status=200)

    assert client.flag(gameId, 0, 0) == board

'''

# TODO. Implement client methods for:
* remove flag
* add/remove question marks
* logout
* gameList

'''