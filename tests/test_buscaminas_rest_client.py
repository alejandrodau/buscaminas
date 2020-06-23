
import pytest
import itertools
import responses
import json

from buscaminas_rest_client import BuscaminasClient, BuscaminasClientException


mockUrl = 'http://testserver:5000/'

# TODO: *********** Test unhappy paths! ***************

@pytest.fixture
def client():
    return BuscaminasClient(mockUrl)


@responses.activate
def test_addUser(client):
    expectedToken = "633e6e3f-43c1-428b-9660-38fe3bb6035c"
    responses.add(responses.POST, mockUrl + '/user/add',
                  json={'token': expectedToken}, status=200)

    client.addUser('pepe', 'pepepass')
    assert client._sessionToken == expectedToken


@responses.activate
def test_login(client):
    expectedToken = "633e6e3f-43c1-428b-9660-38fe3bb6035c"
    responses.add(responses.POST, mockUrl + '/user/login',
                  json={'token': expectedToken}, status=200)

    client.login('pepe', 'pepepass')
    assert client._sessionToken == expectedToken

@responses.activate
def test_badLogin(client):
    responses.add(responses.POST, mockUrl + '/user/login',
                  json={'error': {'errorCode': 'BadUserOrPass'}}, status=400)

    with pytest.raises(BuscaminasClientException):
        client.login('pepe', 'pepepass')


@responses.activate
def test_getBoard(client):
    token = "633e6e3f-43c1-428b-9660-38fe3bb6035c"
    gameId = "75fd6be1-5320-4677-8106-1c71f09af6f1"
    board = json.loads('{"board":[[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."]],"status":"active"}')

    responses.add(responses.POST, mockUrl + '/user/login',
                  json={'token': token}, status=200)
    responses.add(responses.GET, mockUrl + '/board/' + gameId, headers={'Authorization': token},
                  json=board, status=200)

    client.login('pepe', 'pepepass')
    assert client.getBoard(gameId) == board

@responses.activate
def test_newGame(client):
    token = "633e6e3f-43c1-428b-9660-38fe3bb6035c"
    gameId = "75fd6be1-5320-4677-8106-1c71f09af6f1"
    board = json.loads('{"board":[[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."]],"status":"active"}')

    responses.add(responses.POST, mockUrl + '/user/login',
                  json={'token': token}, status=200)
    responses.add(responses.POST, mockUrl + '/newGame', headers={'Authorization': token},
                  json={'gameId': gameId}, status=200)

    client.login('pepe', 'pepepass')
    assert client.newGame(5, 5, 3) == gameId

'''
$ curl -H "Authorization: <token>" -d xsize=5 -d ysize=5 -d mines=3 http://127.0.0.1:5000/newGame
{"gameId":"75fd6be1-5320-4677-8106-1c71f09af6f1"}


curl -X PUT -H "Authorization: <token>" -d x=0 -d y=0 http://127.0.0.1:5000/board/75fd6be1-5320-4677-8106-1c71f09af6f1/uncover
{"board":[[1,".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."]],"status":"active"}

curl -X PUT -H "Authorization: <token>" -d x=0 -d y=1 http://127.0.0.1:5000/board/75fd6be1-5320-4677-8106-1c71f09af6f1/flag
{"board":[[1,"F",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."]],"status":"active"}

# TODO. Implement client methods for:
curl -X PUT -H "Authorization: <token>" -d x=0 -d y=2 http://127.0.0.1:5000/board/75fd6be1-5320-4677-8106-1c71f09af6f1/question
{"board":[[1,"F","?",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."]],"status":"active"}

$ curl -H "Authorization: 633e6e3f-43c1-428b-9660-38fe3bb6035c" -X POST http://127.0.0.1:5000/user/logout
{}

$ curl -H "Authorization: ad4b38da-de85-4b8b-a1fe-d7aae50d2f20" http://127.0.0.1:5000/user/gameList
{"gameList":[]}

'''