import pickle
import uuid


class GameIdNotFound(Exception):
    pass


class MemoryGameStore():
    def __init__(self):
        self._store = {}

    def get(self, gameId):
        try:
            return pickle.loads(self._store[gameId])
        except KeyError:
            raise GameIdNotFound()

    def put(self, gameId, game):
        self._store[gameId] = pickle.dumps(game)

    def new(self, game):
        gameId = str(uuid.uuid4())
        self.put(gameId, game)
        return gameId
