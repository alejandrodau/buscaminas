# Buscaminas

Basic implementation of a Minesweeper game, to play with python3 and flask

## Installation
(TODO)

## Sample usage:

```
>>> import buscaminas
>>> game = buscaminas.Minesweeper(5, 5, 3, 1)
>>> pprint(game.getVisibleBoard())
[['.', '.', '.', '.', '.'],
 ['.', '.', '.', '.', '.'],
 ['.', '.', '.', '.', '.'],
 ['.', '.', '.', '.', '.'],
 ['.', '.', '.', '.', '.']]
>>> game.uncover(0,0)
>>> pprint(game.getVisibleBoard())
[[' ', 1, '.', '.', '.'],
 [' ', 1, 2, 3, '.'],
 [' ', ' ', ' ', 1, 1],
 [' ', ' ', ' ', ' ', ' '],
 [' ', ' ', ' ', ' ', ' ']]
>>> game.putFlag(0,2)
>>> game.putFlag(0,3)
>>> game.putQuestionMark(0,4)
>>> game.putFlag(1,4)
>>> pprint(game.getVisibleBoard())
[[' ', 1, 'F', 'F', '?'],
 [' ', 1, 2, 3, 'F'],
 [' ', ' ', ' ', 1, 1],
 [' ', ' ', ' ', ' ', ' '],
 [' ', ' ', ' ', ' ', ' ']]
>>> game.uncover(0,4)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/avd/src/buscaminas/buscaminas/minesweeper.py", line 87, in uncover
    self.checkVictory()
  File "/home/avd/src/buscaminas/buscaminas/minesweeper.py", line 73, in checkVictory
    raise VictoryException()
buscaminas.minesweeper.VictoryException
>>> pprint(game.getVisibleBoard())
[[' ', 1, '*', '*', 2],
 [' ', 1, 2, 3, '*'],
 [' ', ' ', ' ', 1, 1],
 [' ', ' ', ' ', ' ', ' '],
 [' ', ' ', ' ', ' ', ' ']]

```