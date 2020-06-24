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
* To serve the API, start flask server
```
$ ./app.sh
```

## Game API Entry points
These are the entry points to handle gameplay. Notice that currently token identification is not implemented so not neccesary, but it is shown in the invocation examples so it can be used to support user collection of games.


### /newGame
Create a new game
* methods: POST
* parameters:
	* xsize: board x size
	* ysize: board y size
	* mines: mines to hide in the board
* returns a gameId
```
$ curl -H "Authorization: <token>" -d xsize=5 -d ysize=5 -d mines=3 http://127.0.0.1:5000/newGame
{"gameId":"75fd6be1-5320-4677-8106-1c71f09af6f1"}
```

### /board/:gameId
Get the board state for `gameId`
* methods: GET
* Returns
    * status: active|victory|gameOver
    * board: array of columns, with each column an array of cellcodes:
        * ".": covered cell
        * "F": flagged covered cell
        * "?": covered cell with a question mark:
        * " ": uncovered cell without mines in its neighboring cells
        * 1-8: uncovered cell with n neighboring mines
        * "*": mine (shown once the game is finished)
```
$ curl -H "Authorization: <token>" http://127.0.0.1:5000/board/75fd6be1-5320-4677-8106-1c71f09af6f1
{"board":[[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."]],"status":"active"}
```

### /board/:gameId/uncover
Uncover a cell
* methods: PUT
* parameters:
    * x, y: cell position
* Returns: _status_ and _board_ as described for `/board` call
```
curl -X PUT -H "Authorization: <token>" -d x=0 -d y=0 http://127.0.0.1:5000/board/75fd6be1-5320-4677-8106-1c71f09af6f1/uncover
{"board":[[1,".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."]],"status":"active"}
```

### /board/:gameId/flag
Add/remove a flag on an uncovered cell
* methods: PUT, DELETE
* parameters:
    * x, y: flag position
* Returns: _status_ and _board_ as described for `/board` call
```
curl -X PUT -H "Authorization: <token>" -d x=0 -d y=1 http://127.0.0.1:5000/board/75fd6be1-5320-4677-8106-1c71f09af6f1/flag
{"board":[[1,"F",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."]],"status":"active"}
```

### /board/:gameId/question
Add/remove a question mark on an uncovered cell
* methods: PUT, DELETE
* parameters:
    * x, y: flag position
* Returns: _status_ and _board_ as described for `/board` call
```
curl -X PUT -H "Authorization: <token>" -d x=0 -d y=2 http://127.0.0.1:5000/board/75fd6be1-5320-4677-8106-1c71f09af6f1/question
{"board":[[1,"F","?",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."],[".",".",".",".","."]],"status":"active"}
```

## Multi user API Entry points
Althought not yet implemented, these are the entry points to handle the creation and login of users, and obtaining a game token:

### /user/add
Add user/passwd and return a session token
* methods: POST
* parameters:
	* user
    * passwd
* Returns: token to be used in the `Authentication:` header
```
$ curl -d user=pepe -d passwd=pepepass http://127.0.0.1:5000/user/add
{"token":"633e6e3f-43c1-428b-9660-38fe3bb6035c"}
```

### /user/login
Login and obtain a fresh token
* methods: POST
* parameters:
	* user
    * passwd
```
 curl -d user=pepe -d passwd=pepepass http://127.0.0.1:5000/user/login
{"token":"b785472c-50c7-4e46-bae2-cd8e8246e2c8"}
```

### /user/logout
Invalidate current session token
* methods: POST
```
curl -H "Authorization: 633e6e3f-43c1-428b-9660-38fe3bb6035c" -X POST http://127.0.0.1:5000/user/logout
{}
```

### /user/gameList
Return the list of games for current user. _Not yet implemented_
* methods: GET
```
$ curl -H "Authorization: ad4b38da-de85-4b8b-a1fe-d7aae50d2f20" http://127.0.0.1:5000/user/gameList
{"gameList":[]}
```

## Error codes
If one of the APIs has an error processing a request because of a bad or missing parameter, it will return http error 400, and an structure like `{"error":{"errorCode":<errorCode>}}`, where errorCode can be:

* InvalidOperation: when trying to flag an uncovered cell, for example
* InvalidParameter: missing parameter or value out of range
* GameIdNotFound: when refering to a gameId that is missing or not belinging to the user
* UserAlreadyExists: when trying to create a username that already exists

## Demo server
A demo server is running in http://buscaminas.hopto.org:5555/

## Buscaminas client library
A client library to play the game using the rest api. Sample usage:

```
>>> from buscaminas_rest_client import BuscaminasClient
>>> cl = BuscaminasClient('http://buscaminas.hopto.org:5555/')
>>> cl.addUser('test', 'pass') # this will automatically login the session
>>> gameId = cl.newGame(3, 4, 2)
>>> cl.getBoard(gameId)
{'board': [['.', '.', '.', '.'], ['.', '.', '.', '.'], ['.', '.', '.', '.']], 'status': 'active'}
>>> def boardPrint(response):
...    for v in response['board']: print('\t'.join(v))
...    print("status: ", response['status'])
... 
>>> boardPrint(cl.uncover(gameId,0,0))
1   .   .   .
.   .   .   .
.   .   .   .
status:  active
>>> boardPrint(cl.uncover(gameId,0,1))
1   1   .   .
.   .   .   .
.   .   .   .
status:  active
>>> boardPrint(cl.uncover(gameId,1,1))
1   1   2   *
1   *   2   1
1   1   1    
status:  gameOver

>>> gameId = cl.newGame(4, 4, 2)
>>> boardPrint(cl.uncover(gameId,0,0))
             
2   2   1    
.   .   1    
.   .   1    
status:  active
>>> boardPrint(cl.flag(gameId,2,1))
             
2   2   1    
.   F   1    
.   .   1    
status:  active
>>> boardPrint(cl.flag(gameId,2,0))
             
2   2   1    
F   F   1    
.   .   1    
status:  active
>>> boardPrint(cl.uncover(gameId,3,0))
             
2   2   1    
F   F   1    
2   .   1    
status:  active
>>> boardPrint(cl.uncover(gameId,3,1))
             
2   2   1    
*   *   1    
2   2   1    
status:  victory
>>> 
```
## Buscaminas game module
This project provides the module "buscaminas" that you can use to play the game from a python code or a python cli, like this:

```
>>> # this is only to pritty print boards in this example:
>>> from tabulate import tabulate
>>> def printtab(matrix): print(tabulate(matrix, tablefmt="grid"))
>>>
>>> import buscaminas
>>> game = buscaminas.Buscaminas(5, 5, 3, 1)
>>> pprinttab(game.getVisibleBoard())
+---+---+---+---+---+
| . | . | . | . | . |
+---+---+---+---+---+
| . | . | . | . | . |
+---+---+---+---+---+
| . | . | . | . | . |
+---+---+---+---+---+
| . | . | . | . | . |
+---+---+---+---+---+
| . | . | . | . | . |
+---+---+---+---+---+
>>> game.uncover(0,0)
>>> pprinttab(game.getVisibleBoard())
+--+---+---+---+---+
|  | 1 | . | . | . |
+--+---+---+---+---+
|  | 1 | 2 | 3 | . |
+--+---+---+---+---+
|  |   |   | 1 | 1 |
+--+---+---+---+---+
|  |   |   |   |   |
+--+---+---+---+---+
|  |   |   |   |   |
+--+---+---+---+---+
>>> game.putFlag(0,2)
>>> game.putFlag(0,3)
>>> game.putQuestionMark(0,4)
>>> game.putFlag(1,4)
>>> pprinttab(game.getVisibleBoard())
+--+---+---+---+---+
|  | 1 | F | F | ? |
+--+---+---+---+---+
|  | 1 | 2 | 3 | F |
+--+---+---+---+---+
|  |   |   | 1 | 1 |
+--+---+---+---+---+
|  |   |   |   |   |
+--+---+---+---+---+
|  |   |   |   |   |
+--+---+---+---+---+
>>> game.uncover(0,4)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/avd/src/buscaminas/buscaminas/buscaminas.py", line 87, in uncover
    self.checkVictory()
  File "/home/avd/src/buscaminas/buscaminas/buscaminas.py", line 73, in checkVictory
    raise VictoryException()
buscaminas.buscaminas.VictoryException
>>> pprinttab(game.getVisibleBoard())
+--+---+---+---+---+
|  | 1 | * | * | 2 |
+--+---+---+---+---+
|  | 1 | 2 | 3 | * |
+--+---+---+---+---+
|  |   |   | 1 | 1 |
+--+---+---+---+---+
|  |   |   |   |   |
+--+---+---+---+---+
|  |   |   |   |   |
+--+---+---+---+---+
```
