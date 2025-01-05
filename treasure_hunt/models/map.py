from abc import ABC, abstractmethod
from random import randint


class Map(ABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Map, cls).__new__(cls, *args, **kwargs)
            cls._instance.__initialize()
        return cls._instance

    def __initialize(self) -> None:
        self.map_data = [
            [self._random_treasure_value() for _ in range(self.width)] for _ in range(self.height)
        ]
        self._post_initialize()

    @property
    @abstractmethod
    def height(self) -> int: ...

    @property
    @abstractmethod
    def width(self) -> int: ...

    @abstractmethod
    def _random_treasure_value(self) -> str: ...

    def _post_initialize(self) -> None: ...

    def bounds(self) -> tuple[int, int]:
        return self.height - 1, self.width - 1

    def display(self) -> str:
        result = []
        for row in self.map_data:
            formatted_row = " | ".join(f"{str(cell):>3}" for cell in row)
            result.append(formatted_row)
        return "\n".join(result)

    def matrix(self) -> list[list]:
        rows = self.display().strip().split("\n")
        matrix = [
            [
                int(value.strip()) if value.strip().isdigit() else value.strip()
                for value in row.split("|")
            ]
            for row in rows
        ]
        return matrix

    def update(self, x: int, y: int, value: str | int) -> None:
        self.map_data[x][y] = value


class GameMap(Map):
    @property
    def height(self) -> int:
        return 3

    @property
    def width(self) -> int:
        return 3

    def _random_treasure_value(self) -> str:
        return str(randint(1, 9))

    def _post_initialize(self) -> None:
        x, y = self.bounds()
        self.update(x=randint(0, x), y=randint(0, y), value="X")


class SpecialGameMap(Map):
    @property
    def height(self) -> int:
        return 2

    @property
    def width(self) -> int:
        return 2

    def _random_treasure_value(self) -> str:
        return str(randint(10, 30))
