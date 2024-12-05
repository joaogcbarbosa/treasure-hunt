from typing import Union
from .constants import MAX_PLAYERS, MIN_PLAYERS
from .templates import number_of_players_warn, number_of_players
from time import sleep
from ..server.game_map import game_map
from itertools import product


def check_number_of_players() -> int:
    nro_players = int(input().strip())
    while nro_players > MAX_PLAYERS or nro_players < MIN_PLAYERS:
        number_of_players_warn()
        sleep(1.5)
        number_of_players()
        nro_players = int(input().strip())
    return nro_players


def check_available_positions(positions: list[tuple[int]], game_map: list[list[Union[int, str]]]) -> bool:
    map_positions = []
    for i in range(len(game_map)):
        for j in range(len(game_map)):
            map_positions.append((i, j))

    for p in positions:
        if p not in map_positions:
            positions.remove(p)


def check_player_position(game_map: list[list[Union[int, str]]], player: str) -> tuple[int, int]:
    x: int
    y: int
    for i in range(len(game_map)):
        for j in range(len(game_map)):
            if isinstance(game_map[i][j], str) and game_map[i][j] == player:
                x = i
                y = j
                break

    return x, y


def check_possible_moves(player: str, game_map: list[list[Union[int, str]]]) -> list[str]:
    player_pos = check_player_position(game_map, player)
    x, y = player_pos
    surrounding_positions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    available_positions = check_available_positions(surrounding_positions)
    return surrounding_positions


if __name__ == "__main__":
    map_situation = [
        [2, 2, 2],
        [3, 3, "P1"],
        [4, 5, 6],
    ]
    print(check_possible_moves("P1", map_situation))
