from random import randint
from abc import ABC, abstractmethod

class Map(ABC):
    pass

class GameMap:
    _instance = None
    _HEIGHT = 4
    _WIDTH = 4

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GameMap, cls).__new__(cls, *args, **kwargs)
            cls._instance.__initialize()
        return cls._instance
    
    def __initialize(self) -> None:
        self.game_map = [
            [self.__random_treasure_value() for _ in range(self._HEIGHT)] for _ in range(self._WIDTH)
        ]
        self.__spot_special_room()

    def __random_treasure_value(self) -> str:
        return str(randint(1, 9))

    def __spot_special_room(self) -> None:
        x, y = self.bounds()
        self.update(x=randint(0, x), y=randint(0, y), value="X")

    def bounds(self) -> tuple[int, int]:
        return self._HEIGHT - 1, self._WIDTH - 1

    def display(self) -> str:
        result = []
        for row in self.game_map:
            result.append(" | ".join(row))
        return "\n".join(result)

    def update(self, x: int, y: int, value: str | int) -> None:
        self.game_map[x][y] = value


class SpecialGameMap:
    _instance = None
    _HEIGHT = 5
    _WIDTH = 5

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SpecialGameMap, cls).__new__(cls, *args, **kwargs)
            cls._instance.__initialize()
        return cls._instance
    
    def __initialize(self) -> None:
        self.special_game_map = [
            [self.__random_treasure_value() for _ in range(self._HEIGHT)] for _ in range(self._WIDTH)
        ]

    def __random_treasure_value(self) -> str:
        return str(randint(10, 30))

    def bounds(self) -> tuple[int, int]:
        return self._HEIGHT - 1, self._WIDTH - 1

    def display(self) -> str:
        result = []
        for row in self.special_game_map:
            result.append(" | ".join(row))
        return "\n".join(result) 

    def update(self, x: int, y: int, value: str | int) -> None:
        self.special_game_map[x][y] = value
