from .game_map import game_map
from random import randint

rnd = 0
occupied_spots = []

def spot_players(number_of_players: int) -> None:
    global occupied_spots
    for i in range(1, number_of_players + 1):
        height_bound, width_bound = game_map.bounds()
        height, width = randint(0, height_bound), randint(0, width_bound)
        player = f"P{i}"
        while (height, width) in occupied_spots:
            height, width = randint(0, height_bound), randint(0, width_bound)
        game_map.update(height, width, player)
        occupied_spots.append((height, width, player))
