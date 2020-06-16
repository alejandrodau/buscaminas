import pytest
import itertools
from buscaminas import Minesweeper, GameOverException


xsize = 5
ysize = 10
mines = 4


@pytest.fixture
def game():
    return Minesweeper(xsize=xsize, ysize=ysize, mines=mines, randSeed=1)


def test_newGame(game):
    assert not game.isOver
    board = game.getVisibleBoard()
    for cell in itertools.chain.from_iterable(board):
        assert cell == "."


def test_explodes(game):
    with pytest.raises(GameOverException):
        for x, y in itertools.product(range(xsize), range(ysize)):
            game.uncover(x, y)
    assert game.isOver
