# Buscaminas

Basic implementation of a Minesweeper game, to play with python3 and flask

## Installation
* Clone the repository
* Create virtualenv and install flask:
```
$ virtualenv -p python3 venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```
* Start flask server
```
$ ./app.sh
```

## Buscaminas game module
This project provides the module "buscaminas" that you can use to play the game from a python code or a python cli, like this:

```
>>> import buscaminas
>>> game = buscaminas.Buscaminas(5, 5, 3, 1)
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
  File "/home/avd/src/buscaminas/buscaminas/buscaminas.py", line 87, in uncover
    self.checkVictory()
  File "/home/avd/src/buscaminas/buscaminas/buscaminas.py", line 73, in checkVictory
    raise VictoryException()
buscaminas.buscaminas.VictoryException
>>> pprint(game.getVisibleBoard())
[[' ', 1, '*', '*', 2],
 [' ', 1, 2, 3, '*'],
 [' ', ' ', ' ', 1, 1],
 [' ', ' ', ' ', ' ', ' '],
 [' ', ' ', ' ', ' ', ' ']]

```