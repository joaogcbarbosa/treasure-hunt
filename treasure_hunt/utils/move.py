from random import choice, randint
from time import sleep, time
from typing import Literal

from ..utils.checks import check_possible_moves
from ..utils.converters import string_to_matrix
from ..models.map import GameMap, SpecialGameMap
from ..server.game_map import special_game_map

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
        map_situation = string_to_matrix(game_map.display())
        if map_situation[x][y] == "X":
            global special_game_map
            game_map.update(x, y, player)  # Jogador se moveu
            move_to_special_map(player, coin_db, special_game_map, game_map, (x, y))
            return game_map
        else:
            collect_coin(coin_db, (x, y), game_map, player)
            total_coins = sum(int(elem) for row in map_situation for elem in row if elem != "X" and elem not in ("P1", "P2", "P3"))
            if (
                total_coins == 0 and 
                isinstance(game_map, GameMap) and not
                any("X" in row for row in map_situation)
            ):
                declare_champion(coin_db)
            game_map.update(x, y, player)

        print(f"Jogador {player} coletou {sum(coin_db[player])} pontos.")
        game_map.update(former_x, former_y, "0")  # Jogador coletou a pontuação de onde estava
        return game_map

    print("Could not move.")


def move_to_special_map(
        player: str,
        coin_db: dict[str, list],
        special_game_map: SpecialGameMap,
        game_map: GameMap,
        special_position: tuple[int, int]):
    # Spota jogador no mapa especial
    height_bound, width_bound = special_game_map.bounds()
    height, width = randint(0, height_bound), randint(0, width_bound)
    special_game_map.update(height, width, player)
    # Inicia a contagem de tempo no mapa especial
    start_time = time()
    while True:
        print(special_game_map.display())
        possible_moves, player_pos = check_possible_moves(
            player, 
            string_to_matrix(special_game_map.display())
        )
        print(f"{player} turn:", end=" ")
        player_choice = choice(["w", "a", "s", "d"]).upper()
        # player_choice = input().upper()
        move_player(player_choice, player, possible_moves, player_pos, coin_db, special_game_map)

        # Se passar dos 10s, sai do loop
        if time() - start_time >= 10:
            break

        sleep(1)

    special_map_situation = string_to_matrix(special_game_map.display())
    for i in range(len(special_map_situation)):
        for j in range(len(special_map_situation)):
            if special_map_situation[i][j] == player:
                special_game_map.update(i, j, "0")
    total_coins = sum(int(elem) for row in special_map_situation for elem in row if elem not in ("P1", "P2", "P3"))
    if total_coins != 0:
        game_map.update(special_position[0], special_position[1], "X")


def declare_champion(coin_db: dict[str, list]):
    print("\n")
    for k, v in coin_db.items():
        print(f"{k}: {sum(v)} pontos")