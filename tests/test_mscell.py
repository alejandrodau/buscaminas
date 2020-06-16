import pytest
from buscaminas import MSCell, UncoveredMineException, \
                       CellAlreadyHasMineException


x = 1
y = 3


@pytest.fixture
def cell():
    return MSCell()


def test_MSCell(cell):
    assert cell.count == 0


def test_increment(cell):
    cell.increment()
    assert cell.count == 1
    cell.increment()
    assert cell.count == 2


def test_uncover(cell):
    assert cell.isCovered
    cell.uncover()
    assert not cell.isCovered


def test_explode(cell):
    cell.putMine()
    assert cell.hasMine
    with pytest.raises(UncoveredMineException):
        cell.uncover()
    assert not cell.isCovered


def test_alreadHasMine(cell):
    cell.putMine()
    with pytest.raises(CellAlreadyHasMineException):
        cell.putMine()


def test_flag(cell):
    assert not cell.hasFlag
    cell.putFlag()
    assert cell.hasFlag
    cell.removeFlag()
    assert not cell.hasFlag


def test_isCorrectlyFlagged(cell):
    assert not cell.hasMine
    assert not cell.hasFlag
    assert cell.isCorrectlyFlagged()
    cell.putFlag()
    assert not cell.isCorrectlyFlagged()
    cell.putMine()
    assert cell.isCorrectlyFlagged()
    cell.removeFlag()
    assert not cell.isCorrectlyFlagged()


def test_questionMark(cell):
    assert not cell.hasQuestionMark
    cell.putQuestionMark()
    assert cell.hasQuestionMark
    cell.removeQuestionMark()
    assert not cell.hasQuestionMark
