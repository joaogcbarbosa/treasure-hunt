from treasure_hunt.models.map import GameMap
from treasure_hunt.utils.converters import string_to_matrix

from random import sample

def spot_players(number_of_players: int, game_map: GameMap) -> None:
    map_situation = string_to_matrix(game_map.display())
    all_positions = [
        (height, width) 
        for height in range(game_map.bounds()[0]) 
        for width in range(game_map.bounds()[1])
        if map_situation[height][width] != "X"  # Filtra posições com "X"
    ]
    
    # Garante que há posições disponíveis suficientes
    if len(all_positions) < number_of_players:
        raise ValueError("Não há posições disponíveis suficientes para todos os jogadores.")
    
    occupied_positions = sample(all_positions, number_of_players)
    
    for i, (height, width) in enumerate(occupied_positions, start=1):
        player = f"P{i}"
        game_map.update(height, width, player)
