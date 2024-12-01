from random import randint

class GameMap:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GameMap, cls).__new__(cls, *args, **kwargs)
            cls._instance.initialize()
        return cls._instance
    
    def _random_treasure_value(self) -> str:
        return str(randint(1, 10))

    def initialize(self):
        self.map = [
            [self._random_treasure_value()] * 4,
            [self._random_treasure_value()] * 4,
            [self._random_treasure_value()] * 4,
            [self._random_treasure_value()] * 4,
        ]

    def display(self):
        for row in self.map:
            print(" | ".join(row))
        print("\n")

    def update(self, x, y, value):
        self.map[x][y] = value
