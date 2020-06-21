from flask import Flask, jsonify, request


from buscaminas import Minesweeper, GameOverException,\
                       VictoryException, InvalidOperationException
from .gamestore import MemoryGameStore, GameIdNotFound


app = Flask(__name__)


gameStore = MemoryGameStore()


@app.errorhandler(IndexError)
def indexError_handler(error):
    return jsonify(error={'errorCode': 'IndexError'}), 400


@app.errorhandler(InvalidOperationException)
def invalidOperationError_handler(error):
    return jsonify(error={'errorCode': 'InvalidOperation'}), 400


@app.errorhandler(KeyError)
def keyError_handler(error):
    return jsonify(error={'errorCode': 'InvalidParameter'}), 400


@app.errorhandler(GameIdNotFound)
def gameIdNotFoundError_handler(error):
    return jsonify(error={'errorCode': 'GameIdNotFound'}), 400


@app.route('/')
def buscaminas_api():
    return 'Hello, this is the buscaminas api!'


def reset_state(gameId, xsize, ysize, mines, seed):
    global gameStore
    gameStore = MemoryGameStore()
    game = Minesweeper(xsize, ysize, mines, seed)
    gameStore.put(gameId, game)


def getStatusCode(game):
    if game.isOver:
        if game.isWin:
            return 'victory'
        else:
            return 'gameOver'
    return 'active'


def getCoords(args):
    x = int(args.get('x'))
    y = int(args.get('y'))
    return x, y


@app.route('/board/<gameId>', methods=['GET'])
def board(gameId):
    game = gameStore.get(gameId)
    return jsonify(status=getStatusCode(game), board=game.getVisibleBoard())


@app.route('/board/<gameId>/uncover', methods=['PUT'])
def uncover(gameId):
    game = gameStore.get(gameId)
    try:
        x, y = getCoords(request.args)
        game.uncover(x, y)
    except GameOverException:
        pass
    except VictoryException:
        pass
    gameStore.put(gameId, game)
    return jsonify(status=getStatusCode(game), board=game.getVisibleBoard())


@app.route('/board/<gameId>/flag', methods=['PUT'])
def flag(gameId):
    game = gameStore.get(gameId)
    try:
        x, y = getCoords(request.args)
        game.putFlag(x, y)
    except GameOverException:
        pass
    except VictoryException:
        pass
    gameStore.put(gameId, game)
    return jsonify(status=getStatusCode(game), board=game.getVisibleBoard())


@app.route('/board/<gameId>/question', methods=['PUT'])
def question(gameId):
    game = gameStore.get(gameId)
    x, y = getCoords(request.args)
    game.putQuestionMark(x, y)
    gameStore.put(gameId, game)
    return jsonify(status=getStatusCode(game), board=game.getVisibleBoard())


@app.route('/board/<gameId>/question', methods=['DELETE'])
def question_delete(gameId):
    game = gameStore.get(gameId)
    x, y = getCoords(request.args)
    game.removeQuestionMark(x, y)
    gameStore.put(gameId, game)
    return jsonify(status=getStatusCode(game), board=game.getVisibleBoard())


@app.route('/board/<gameId>/flag', methods=['DELETE'])
def flag_delete(gameId):
    game = gameStore.get(gameId)
    x, y = getCoords(request.args)
    game.removeFlag(x, y)
    gameStore.put(gameId, game)
    return jsonify(status=getStatusCode(game), board=game.getVisibleBoard())


@app.route('/newGame', methods=['POST'])
def newGame():
    xsize = int(request.args.get('xsize'))
    ysize = int(request.args.get('ysize'))
    mines = int(request.args.get('mines'))
    game = Minesweeper(xsize, ysize, mines)
    return jsonify(gameId=gameStore.new(game))
