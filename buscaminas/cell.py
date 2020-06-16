
class CellAlreadyHasMineException(Exception):
    pass


class UncoveredMineException(Exception):
    pass


class MSCell():
    """ Minesweeper cell modeling class """
    def __init__(self, count=0, hasMine=False, isCovered=True,
                 hasFlag=False, hasQuestionMark=False):
        self._count = count
        self._hasMine = hasMine
        self._isCovered = isCovered
        self._hasFlag = hasFlag
        self._hasQuestionMark = hasQuestionMark

    @property
    def count(self):
        """ count of neighboring mines """
        return self._count

    def increment(self):
        """ increment the neighboring mines count """
        self._count += 1

    @property
    def hasFlag(self):
        """ cell is flagged? """
        return self._hasFlag

    def putFlag(self):
        """ put a flag in cell """
        self._hasFlag = True

    def removeFlag(self):
        """ remove a flag from cell """
        self._hasFlag = False

    @property
    def hasQuestionMark(self):
        """ cell has question mark? """
        return self._hasQuestionMark

    def putQuestionMark(self):
        """ put a question mark in cell """
        self._hasQuestionMark = True

    def removeQuestionMark(self):
        """ remove question mark from cell """
        self._hasQuestionMark = False

    @property
    def hasMine(self):
        """ is there a mine in this cell? """
        return self._hasMine

    def putMine(self):
        """ put a mine in this cell """
        if self.hasMine:
            raise CellAlreadyHasMineException()
        self._hasMine = True

    @property
    def isCovered(self):
        """ is this cell covered? """
        return self._isCovered

    def uncover(self):
        """ uncover this cell. Raises exception if it has a mine! """
        self._isCovered = False
        if self.hasMine:
            raise UncoveredMineException()

    def isCorrectlyFlagged(self):
        """ is this cell correctly flaggged """
        return (self.hasMine and self.hasFlag or
                not self.hasMine and not self.hasFlag)
