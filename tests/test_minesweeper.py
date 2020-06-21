import pytest
import itertools
from buscaminas import Minesweeper, GameOverException,\
                       VictoryException, InvalidOperationException
from buscaminas.cellcode import COVERED, BLANK, FLAG, QUESTION


xsize = 5
ysize = 5
mines = 3


@pytest.fixture
def game():
    return Minesweeper(xsize=xsize, ysize=ysize, mines=mines, randSeed=1)


def test_newGame(game):
    assert not game.isOver
    board = game.getVisibleBoard()
    for cell in itertools.chain.from_iterable(board):
        assert cell == COVERED


def test_explodes(game):
    with pytest.raises(GameOverException):
        game.uncover(0, 2)
    assert game.isOver
    checkBoardIsCleared(game)


def checkBoardIsCleared(game):
    board = game.getVisibleBoard()
    for cell in itertools.chain.from_iterable(board):
        assert cell != COVERED
        assert cell != FLAG
        assert cell != QUESTION


def test_autoUncover(game):
    game.uncover(0, 0)
    board = game.getVisibleBoard()
    assert board[0] == [BLANK, 1, COVERED, COVERED, COVERED]
    assert board[1] == [BLANK, 1, 2, 3, COVERED]
    assert board[2] == [BLANK, BLANK, BLANK, 1, 1]
    assert board[3] == [BLANK, BLANK, BLANK, BLANK, BLANK]
    assert board[4] == [BLANK, BLANK, BLANK, BLANK, BLANK]


def test_victory(game):
    game.uncover(0, 0)
    game.putFlag(0, 2)
    game.putFlag(0, 3)
    game.putFlag(1, 4)
    game.putQuestionMark(0, 4)
    with pytest.raises(VictoryException):
        game.uncover(0, 4)
    checkBoardIsCleared(game)


def test_victoryFlag(game):
    game.uncover(0, 0)
    game.putFlag(0, 2)
    game.putFlag(0, 3)
    game.putFlag(1, 4)
    game.putQuestionMark(0, 4)
    game.removeFlag(0, 2)
    game.uncover(0, 4)
    with pytest.raises(VictoryException):
        game.putFlag(0, 2)
    checkBoardIsCleared(game)


def test_invalidOpsFlag(game):
    game.uncover(0, 0)
    with pytest.raises(InvalidOperationException):
        game.putFlag(0, 0)
    with pytest.raises(InvalidOperationException):
        game.putQuestionMark(0, 0)
