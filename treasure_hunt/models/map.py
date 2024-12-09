from random import randint

class GameMap:
    _instance = None
    # TODO: map bounds could be set by user?
    _HEIGHT = 4
    _WIDTH = 4

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GameMap, cls).__new__(cls, *args, **kwargs)
            cls._instance.__initialize()
        return cls._instance
    
    def __random_treasure_value(self) -> str:
        return str(randint(1, 9))
    
    def bounds(self) -> tuple[int, int]:
        return self._HEIGHT - 1, self._WIDTH - 1

    def __initialize(self):
        self.game_map = [
            [self.__random_treasure_value() for _ in range(4)],
            [self.__random_treasure_value() for _ in range(4)],
            [self.__random_treasure_value() for _ in range(4)],
            [self.__random_treasure_value() for _ in range(4)],
        ]

    def display(self) -> str:
        result = []
        for row in self.game_map:
            result.append(" | ".join(row))
        return "\n".join(result) 

    def update(self, x: int, y: int, value: str | int):
        self.game_map[x][y] = value
