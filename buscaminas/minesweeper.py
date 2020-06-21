from .board import MSBoard
from .cell import UncoveredMineException
from . import cellcode
import itertools


class InvalidOperationException(Exception): pass


class VictoryException(Exception): pass


class GameOverException(Exception): pass


class Minesweeper():
    """ Minesweeper game class """
    def __init__(self, xsize=0, ysize=0, mines=0, randSeed=None):
        self._board = MSBoard(
            xsize=xsize, ysize=ysize, mines=mines, randSeed=randSeed)
        self._mines = mines
        self._boardSize = xsize * ysize
        self._isOver = False
        self._flagCount = 0
        self._uncoveredCount = 0

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

    def putQuestionMark(self, x, y):
        cell = self._board.cell(x, y)
        if cell.isCovered:
            cell.putQuestionMark()
        else:
            raise InvalidOperationException()

    def putFlag(self, x, y):
        cell = self._board.cell(x, y)
        if cell.isCovered:
            cell.putFlag()
            self._flagCount += 1
            self.checkVictory()
        else:
            raise InvalidOperationException()

    def checkVictory(self):
        if self._flagCount == self._mines and \
           self._uncoveredCount + self._flagCount == self._boardSize:
            self._uncoverBoard()
            raise VictoryException()

    def removeFlag(self, x, y):
        cell = self._board.cell(x, y)
        if cell.hasFlag:
            cell.removeFlag()
            self._flagCount -= 1
            self.checkVictory()

    def removeQuestionMark(self, x, y):
        self._board.cell(x, y).removeQuestionMark()

    def uncover(self, x, y):
        self._uncoveredCount += self._uncover(x, y)
        self.checkVictory()

    def _uncover(self, x, y):
        """ uncover a cell """
        cell = self._board.cell(x, y)
        if not cell.isCovered:
            return 0

        try:
            cell.uncover()
        except UncoveredMineException:
            self._isOver = True
            self._uncoverBoard()
            raise GameOverException()

        uncoverCount = 1
        if cell.count == 0:
            for nx, ny in self._board.neighborCells(x, y):
                uncoverCount += self._uncover(nx, ny)

        return uncoverCount

    def _uncoverBoard(self):
        for cell in itertools.chain.from_iterable(self._board.grid):
            try:
                cell.removeFlag()
                cell.removeQuestionMark()
                cell.uncover()
            except UncoveredMineException:
                pass
