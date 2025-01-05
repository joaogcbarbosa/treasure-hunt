from treasure_hunt.models.map import GameMap, SpecialGameMap

from random import sample, choice

def spot_players(players: list[str], game_map: GameMap | SpecialGameMap) -> None:
    number_of_players = len(players)
    map_situation = game_map.matrix()
    all_positions = [
        (height, width) 
        for height in range(game_map.bounds()[0] + 1) 
        for width in range(game_map.bounds()[1] + 1)
        if map_situation[height][width] != "X"  # Filtra posições com "X"
    ]
        
    occupied_positions = sample(all_positions, number_of_players)
    
    if isinstance(game_map, SpecialGameMap):
        new_position = choice(all_positions)
        height, width = new_position
        game_map.update(height, width, players[0])
        return
    
    for i, (height, width) in enumerate(occupied_positions, start=1):
        player = f"P{i}"
        game_map.update(height, width, player)
