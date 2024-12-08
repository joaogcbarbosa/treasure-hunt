from typing import Literal
from ..models.map import GameMap


def move_player(
    choice: Literal["W", "A", "S", "D"],
    possible_moves: list[tuple[int]],
    player_position: tuple[int, int],
    game_map: GameMap,
):
    x, y = player_position

    deltas = {
        "W": (-1, 0),  # Cima
        "A": (0, -1),  # Esquerda
        "S": (1, 0),   # Baixo
        "D": (0, 1),   # Direita
    }

    dx, dy = deltas[choice]

    new_position = (x + dx, y + dy)

    if new_position in possible_moves:
        x, y = new_position[0], new_position[1]
        game_map.update(x, y, "P1")
        return

    print("Could not move.")
