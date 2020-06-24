
import pytest
import itertools

from buscaminas_rest import buscaminas_rest
from buscaminas.cellcode import COVERED, BLANK, FLAG, QUESTION


xsize = 5
ysize = 5
mines = 3
gameId = 'testing'


@pytest.fixture
def client():
    buscaminas_rest.app.config['TESTING'] = True

    with buscaminas_rest.app.test_client() as client:
        with buscaminas_rest.app.app_context():
            buscaminas_rest.reset_state(gameId, xsize, ysize, mines, 1)
        yield client


def putAndGetBoard(client, route):
    return client.put(route).get_json()['board']


def getBoard(client, gameId):
    return client.get(f'/board/{gameId}').get_json()['board']


def test_newGame(client):
    rv = client.post(f'/newGame?xsize={xsize}&ysize={ysize}&mines={mines}')
    data = rv.get_json()
    newGameId = data['gameId']
    assert gameId is not None
    rv = client.get(f'/board/{newGameId}')
    data = rv.get_json()
    board = data['board']
    assert len(board) == xsize
    for column in board:
        assert len(column) == ysize
    assert data['status'] == 'active'


def test_uncover(client):
    board = getBoard(client, gameId)
    for cell in itertools.chain.from_iterable(board):
        assert cell == COVERED
    board = putAndGetBoard(client, f'/board/{gameId}/uncover?x=0&y=0')
    assert board[0][0] == BLANK


def test_putFlag(client):
    board = getBoard(client, gameId)
    assert board[0][0] != FLAG
    board = putAndGetBoard(client, f'/board/{gameId}/flag?x=0&y=0')
    assert board[0][0] == FLAG


def test_putQuestionMark(client):
    board = getBoard(client, gameId)
    assert board[0][0] != QUESTION
    board = putAndGetBoard(client, f'/board/{gameId}/question?x=0&y=0')
    assert board[0][0] == QUESTION


def test_removeFlag(client):
    board = putAndGetBoard(client, f'/board/{gameId}/flag?x=0&y=0')
    assert board[0][0] == FLAG
    rv = client.delete(f'/board/{gameId}/flag?x=0&y=0')
    board = rv.get_json()['board']
    assert board[0][0] == COVERED


def test_removeQuestion(client):
    board = putAndGetBoard(client, f'/board/{gameId}/question?x=0&y=0')
    assert board[0][0] == QUESTION
    rv = client.delete(f'/board/{gameId}/question?x=0&y=0')
    board = rv.get_json()['board']
    assert board[0][0] == COVERED


def test_gameOver(client):
    rv = client.put(f'/board/{gameId}/uncover?x=0&y=0')
    assert rv.get_json()['status'] == 'active'
    rv = client.put(f'/board/{gameId}/uncover?x=0&y=3')
    assert rv.get_json()['status'] == 'gameOver'


def test_victory(client):
    rv = client.put(f'/board/{gameId}/uncover?x=0&y=0')
    assert rv.get_json()['status'] == 'active'
    rv = client.put(f'/board/{gameId}/flag?x=0&y=2')
    assert rv.get_json()['status'] == 'active'
    rv = client.put(f'/board/{gameId}/flag?x=0&y=3')
    assert rv.get_json()['status'] == 'active'
    rv = client.put(f'/board/{gameId}/flag?x=1&y=4')
    assert rv.get_json()['status'] == 'active'
    rv = client.put(f'/board/{gameId}/uncover?x=0&y=4')
    assert rv.get_json()['status'] == 'victory'


def test_invalidOperation(client):
    rv = client.put(f'/board/{gameId}/uncover?x=0&y=0')
    rv = client.put(f'/board/{gameId}/flag?x=0&y=0')
    assert rv.get_json()['error']['errorCode'] == 'InvalidOperation'


def test_indexError(client):
    rv = client.put(f'/board/{gameId}/uncover?x=100&y=0')
    assert rv.get_json()['error']['errorCode'] == 'IndexError'


'''
# TODO. User and session management!!
'''
