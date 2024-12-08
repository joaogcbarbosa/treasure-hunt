from typing import Literal

from treasure_hunt.utils.converters import string_to_matrix
from ..models.map import GameMap

def collect_coin(
    coin_db: dict[str, list], 
    coin_position: tuple[int, int], 
    game_map: GameMap,
    player: str,
):
    map_situation = string_to_matrix(game_map.display())
    coin_db[player].append(int(map_situation[coin_position[0]][coin_position[1]]))


def move_player(
    choice: Literal["W", "A", "S", "D"],
    player: str,
    possible_moves: list[tuple[int]],
    player_position: tuple[int, int],
    coin_db: dict[str, list],
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
        former_x, former_y = x, y
        x, y = new_position[0], new_position[1]
        collect_coin(coin_db, (x, y), game_map, player)
        print(f"Jogador {player} coletou {sum(coin_db[player])} pontos.")
        game_map.update(former_x, former_y, "0")  # Jogador coletou a pontuação de onde estava
        game_map.update(x, y, player)  # Jogador se moveu
        return game_map

    print("Could not move.")
