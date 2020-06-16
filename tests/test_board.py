import pytest
from buscaminas import MSBoard, MSCell, CellAlreadyHasMineException


xsize = 5
ysize = 10
mines = 4


@pytest.fixture
def board():
    return MSBoard(xsize=xsize, ysize=ysize, mines=mines)


def test_newBoard(board):
    assert board.flags == 0
    assert board.xsize == xsize
    assert board.ysize == ysize
    assert board.mines == mines


def test_mineLocations(board):
    mineCount = 0
    for column in board.grid:
        for cell in column:
            mineCount += 1 if cell.hasMine else 0
    assert mineCount == mines


def test_getGrid(board):
    grid = board.grid
    assert len(grid) == xsize
    for column in grid:
        assert len(column) == ysize
        assert all([isinstance(c, MSCell) for c in column])


def test_addMine():
    board = MSBoard(xsize=xsize, ysize=ysize, mines=0)
    for column in board.grid:
        for cell in column:
            assert cell.count == 0
    board.addMine(0, 0)
    assert board.cell(0, 1).count == 1
    assert board.cell(1, 1).count == 1
    assert board.cell(1, 0).count == 1
    with pytest.raises(CellAlreadyHasMineException):
        board.addMine(0, 0)
    assert board.cell(0, 1).count == 1
    assert board.cell(1, 1).count == 1
    assert board.cell(1, 0).count == 1
    board.addMine(1, 1)
    assert board.cell(0, 1).count == 2
    assert board.cell(0, 2).count == 1
    assert board.cell(1, 0).count == 2
    assert board.cell(1, 2).count == 1
    assert board.cell(2, 0).count == 1
    assert board.cell(2, 1).count == 1
    assert board.cell(2, 2).count == 1
    board.addMine(xsize-1, ysize-1)
    assert board.cell(xsize-2, ysize-1).count == 1
    assert board.cell(xsize-1, ysize-2).count == 1
    assert board.cell(xsize-2, ysize-2).count == 1
