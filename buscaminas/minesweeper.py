from .board import MSBoard
from .cell import UncoveredMineException
from . import cellcode


class GameOverException(Exception):
    pass


class Minesweeper():
    """ Minesweeper game class """
    def __init__(self, xsize=0, ysize=0, mines=0, randSeed=None):
        self._board = MSBoard(
            xsize=xsize, ysize=ysize, mines=mines, randSeed=randSeed)
        self._isOver = False

    @property
    def isOver(self):
        """ is the game over? """
        return self._isOver

    def getVisibleBoard(self):
        """ get a coded representation of the current board """
        visibleBoard = []
        for column in self._board.grid:
            visibleColumn = []
            for cell in column:
                visibleColumn.append(self._getCellCode(cell))
            visibleBoard.append(visibleColumn)
        return visibleBoard

    def _getCellCode(self, cell):
        if cell.hasFlag:
            return cellcode.FLAG
        if cell.hasQuestionMark:
            return cellcode.QUESTION
        if cell.isCovered:
            return cellcode.COVERED
        if cell.hasMine:
            return cellcode.MINE
        return cellcode.count(cell.count)

    def uncover(self, x, y):
        """ uncover a cell """
        cell = self._board.cell(x, y)
        if not cell.isCovered:
            return

        try:
            cell.uncover()
        except UncoveredMineException:
            self._isOver = True
            raise GameOverException()

        if cell.count == 0:
            for nx, ny in self._board.neighborCells(x, y):
                self.uncover(nx, ny)
