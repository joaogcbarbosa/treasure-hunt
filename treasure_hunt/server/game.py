from random import choice, sample

from treasure_hunt.map import GameMap, SpecialGameMap


def spot_players(players: list[str], game_map: GameMap | SpecialGameMap) -> None:
    """
    Função responsável por colocar os players aleatoriamente no mapa principal ou especial,
    respeitando as posições já ocupadas por jogadores e o mapa especial ("X").
    """
    number_of_players = len(players)
    map_situation = game_map.matrix()
    height, width = game_map.bounds()
    all_positions = [
        (h, w)
        for h in range(height + 1)
        for w in range(width + 1)
        if map_situation[h][w] != "X"
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
