
from random import randrange, seed
from .cell import MSCell, CellAlreadyHasMineException


class MSBoard():
    """ Minesweeper board class """

    def __init__(self, xsize, ysize, mines, randSeed=None):
        if xsize < 1:
            raise ValueError("Board xsize too small")
        if ysize < 1:
            raise ValueError("Board ysize too small")
        if mines >= xsize * ysize:
            raise ValueError("Invalid mine count for board")
        if randSeed:
            seed(randSeed)

        self.xsize = xsize
        self.ysize = ysize
        self.mines = mines
        self._grid = self._buildGrid()
        self.flags = 0
        self._putRandomMines(mines)

    def _putRandomMines(self, mines):
        mineCount = 0
        while mineCount < mines:
            try:
                self.addMine(randrange(self.xsize), randrange(self.ysize))
                mineCount += 1
            except CellAlreadyHasMineException:
                pass

    def cell(self, x, y):
        """ Return the cell in a coordinate """
        return self.grid[x][y]

    def _buildGrid(self):
        grid = [
            [MSCell() for _ in range(self.ysize)]
            for _ in range(self.xsize)]
        return grid

    @property
    def grid(self):
        """ Returns the cell grid """
        return self._grid

    def addMine(self, x, y):
        """ Add a mine to the grid board """
        self.cell(x, y).putMine()
        self._incrementAround(x, y)

    def _incrementAround(self, x, y):
        for px, py in self.neighborCells(x, y):
            self.cell(px, py).increment()

    def neighborCells(self, x, y):
        for px in range(max(0, x-1), min(x+2, self.xsize)):
            for py in range(max(0, y-1), min(y+2, self.ysize)):
                if px != x or py != y:
                    yield (px, py)
