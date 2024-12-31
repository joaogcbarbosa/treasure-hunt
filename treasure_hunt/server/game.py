from random import randint

from treasure_hunt.models.map import GameMap
from treasure_hunt.utils.converters import string_to_matrix


def spot_players(number_of_players: int, game_map: GameMap) -> None:
    occupied_spots = []
    for i in range(1, number_of_players + 1):
        height_bound, width_bound = game_map.bounds()
        height, width = randint(0, height_bound), randint(0, width_bound)
        player = f"P{i}"
        map_situation = string_to_matrix(game_map.display())
        while (height, width) in occupied_spots or map_situation[height][width] == "X":
            height, width = randint(0, height_bound), randint(0, width_bound)
        game_map.update(height, width, player)
        occupied_spots.append((height, width, player))
