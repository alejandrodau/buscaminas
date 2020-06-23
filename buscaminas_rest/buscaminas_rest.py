from contextlib import contextmanager
from flask import Flask, jsonify, request


from buscaminas import Buscaminas, GameOverException,\
                       VictoryException, InvalidOperationException
from .gamestore import GameIdNotFound, gameStoreFactory
from .userdb import UserDB, UserAlreadyExists, BadUserOrPass


app = Flask(__name__)


gameStore = gameStoreFactory()
userDB = UserDB()


@app.errorhandler(IndexError)
def indexError_handler(error):
    return _errorCode('IndexError')


@app.errorhandler(InvalidOperationException)
def invalidOperationError_handler(error):
    return _errorCode('InvalidOperation')


@app.errorhandler(BadUserOrPass)
def badUserError_handler(error):
    return _errorCode('BadUserOrPass')


@app.errorhandler(KeyError)
def keyError_handler(error):
    return _errorCode('InvalidParameter')


@app.errorhandler(GameIdNotFound)
def gameIdNotFoundError_handler(error):
    return _errorCode('GameIdNotFound')


@app.errorhandler(UserAlreadyExists)
def userAlreadyExists_handler(error):
    return _errorCode('UserAlreadyExists')


def _errorCode(errorCode):
    return jsonify(error={'errorCode': errorCode}), 400


def reset_state(gameId, xsize, ysize, mines, seed):
    ''' used to create a predictable environment for tests '''
    global gameStore
    gameStore = gameStoreFactory(type='memory')
    game = Buscaminas(xsize, ysize, mines, seed)
    gameStore.put(gameId, game)


def _getStatusCode(game):
    ''' get the status of a game: victory|gameOver|active '''
    if game.isOver:
        if game.isWin:
            return 'victory'
        else:
            return 'gameOver'
    return 'active'


def _getCoords(args):
    x = int(args.get('x'))
    y = int(args.get('y'))
    return x, y


@app.route('/')
def buscaminas_api():
    return 'Hello, this is the buscaminas api!'


def _game_status_response(game):
    return jsonify(status=_getStatusCode(game), board=game.getVisibleBoard())


@contextmanager
def stored_game(gameId):
    game = gameStore.get(gameId)
    try:
        yield game
    finally:
        gameStore.put(gameId, game)


@app.route('/board/<gameId>', methods=['GET'])
def board(gameId):
    '''
    Get the board state
    Returns
        status: active|victory|gameOver
        board: array of columns, with each column an array of cellcodes:
            ".": covered cell
            "F": flagged covered cell
            "?": covered cell with a question mark:
            " ": uncovered cell without mines in its neighboring cells
            1-8: uncovered cell with n neighboring mines
            "*": mine (shown once the game is finished)
    '''
    with stored_game(gameId) as game:
        return _game_status_response(game)


@app.route('/board/<gameId>/uncover', methods=['PUT'])
def uncover(gameId):
    '''
    Uncover a cell
    parameters:
        x, y: cell position
    '''
    with stored_game(gameId) as game:
        try:
            x, y = _getCoords(request.values)
            game.uncover(x, y)
        except GameOverException:
            pass
        except VictoryException:
            pass
        return _game_status_response(game)


@app.route('/board/<gameId>/flag', methods=['PUT'])
def flag(gameId):
    '''
    Add a flag
    parameters:
        x, y: flag position
    '''
    with stored_game(gameId) as game:
        try:
            x, y = _getCoords(request.values)
            game.putFlag(x, y)
        except GameOverException:
            pass
        except VictoryException:
            pass
        return _game_status_response(game)


@app.route('/board/<gameId>/question', methods=['PUT'])
def question(gameId):
    '''
    Add a question mark
    parameters:
        x, y: question mark position
    '''
    with stored_game(gameId) as game:
        x, y = _getCoords(request.values)
        game.putQuestionMark(x, y)
        return _game_status_response(game)


@app.route('/board/<gameId>/question', methods=['DELETE'])
def question_delete(gameId):
    '''
    Remove a question mark
    parameters:
        x, y: question mark position
    '''
    with stored_game(gameId) as game:
        x, y = _getCoords(request.values)
        game.removeQuestionMark(x, y)
        return _game_status_response(game)


@app.route('/board/<gameId>/flag', methods=['DELETE'])
def flag_delete(gameId):
    '''
    Remove a flag
    parameters:
        x, y: flag position
    '''
    with stored_game(gameId) as game:
        x, y = _getCoords(request.values)
        game.removeFlag(x, y)
        return _game_status_response(game)


@app.route('/newGame', methods=['POST'])
def newGame():
    '''
    Create a new game
    parameters:
        xsize: board x size
        ysize: board y size
        mines: mines to hide in the board
    '''
    xsize = int(request.values.get('xsize'))
    ysize = int(request.values.get('ysize'))
    mines = int(request.values.get('mines'))
    game = Buscaminas(xsize, ysize, mines)
    return jsonify(gameId=gameStore.new(game))


# ------------------------------
# session related entry points (for future multi user implementation)
# ------------------------------
@app.route('/user/add', methods=['POST'])
def addUser():
    '''
    Add user/passwd and return a session token
    parameters:
        user
        passwd
    '''
    # TODO: mock implementation - do error handling
    user = request.form['user']
    passwd = request.form['passwd']
    token = userDB.addUser(user, passwd)
    return jsonify(token=token)


@app.route('/user/login', methods=['POST'])
def login():
    '''
    Get a session token
    parameters:
        user
        passwd
    '''
    # TODO: mock implementation - do error handling
    user = request.form['user']
    passwd = request.form['passwd']
    token = userDB.login(user, passwd)
    return jsonify(token=token)


@app.route('/user/logout', methods=['POST'])
def logout():
    '''
    Invalidate current session token
    '''
    userDB.logout(_getToken())
    return jsonify()


@app.route('/user/gameList', methods=['GET'])
def getGameList():
    '''
    Return the list of games for current user
    '''
    return jsonify(gameList=userDB.getGameList(_getToken()))


def _getToken():
    return request.headers.get('Authorization')
