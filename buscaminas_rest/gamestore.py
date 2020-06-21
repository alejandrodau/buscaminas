import pickle
import uuid


def gameStoreFactory(type='memory'):
    if type == 'memory':
        return MemoryGameStore()
        return
    # for now, only MemoryGameStore is implemented
    # TODO: implement persistent GameStore (using redis if available, etc)
    return MemoryGameStore()


class MemoryGameStore():
    def __init__(self):
        self._store = {}

    def get(self, gameId):
        ''' Get a game from the db '''
        try:
            return pickle.loads(self._store[gameId])
        except KeyError:
            raise GameIdNotFound()

    def put(self, gameId, game):
        ''' Update a game '''
        self._store[gameId] = pickle.dumps(game)

    def new(self, game):
        ''' Create a new game entry, return the gameId '''
        gameId = str(uuid.uuid4())
        self.put(gameId, game)
        return gameId


class GameIdNotFound(Exception):
    pass
