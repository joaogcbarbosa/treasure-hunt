from itertools import product
from queue import Queue
from random import choice
from threading import BoundedSemaphore, Lock
from time import sleep, time
from typing import Literal

from ..models.map import GameMap, SpecialGameMap
from ..server.game import spot_players
from ..utils.checks import check_possible_moves
from ..utils.constants import KEYBOARD_OPTIONS
from ..utils.logger import write_log
from ..utils.templates import show_map

special_game_map = SpecialGameMap()
queue_lock: Lock = Lock()
check_semaphore = BoundedSemaphore()
special_map_is_empty: bool = False


def collect_coin(
    coin_db: dict[str, list],
    coin_position: tuple[int, int],
    game_map: GameMap | SpecialGameMap,
    player: str,
):
    map_situation = game_map.matrix()
    coin_db[player].append(int(map_situation[coin_position[0]][coin_position[1]]))


def player_back_to_map(
    players: list[str],
    player_in_special_map: str,
    map_semaphore: BoundedSemaphore,
    game_map: GameMap,
):
    players = set(players)
    players = players - {player_in_special_map}
    map_semaphore.acquire()
    map_situation = game_map.matrix()
    for i, j in product(range(len(map_situation)), range(len(map_situation))):
        if map_situation[i][j] not in players and map_situation[i][j] != "X":
            game_map.update(i, j, player_in_special_map)
            break
    map_semaphore.release()


def handle_special_map_queue(
    special_map_queue: Queue,
    map_semaphore: BoundedSemaphore,
    special_map_semaphore: BoundedSemaphore,
    player: str,
) -> str:
    global queue_lock, special_map_is_empty
    next_player_to_special_map: str = ""  # player
    with queue_lock:
        write_log(f"{player} EM ESPERA OCUPADA")
        special_map_queue.put(player)  # Põe jogador na fila para o mapa especial
        map_semaphore.release()  # Jogadores que entram para a fila do mapa especial ficam em espera ocupada, então param de alterar o mapa principal
    while True:
        check_semaphore.acquire()  # Semáforo para uma thread de cada vez checar se o semáforo do mapa especial foi liberado
        if special_map_semaphore._value != 0:
            next_player_to_special_map = (
                special_map_queue.get()
            )  # Se o semáforo do mapa especial foi liberado então o próximo da fila é resgatado
            map_semaphore.acquire()  # Faz acquire para o mapa principal para realizar o movimento de entrada no mapa especial
            special_map_semaphore.acquire()
            check_semaphore.release()
            break
        elif special_map_is_empty:
            check_semaphore.release()
            return
        check_semaphore.release()
    write_log(f"{next_player_to_special_map} SAIU DA ESPERA OCUPADA")
    return next_player_to_special_map


def get_total_coins(players: list[str], game_map: GameMap | SpecialGameMap):
    map_situation = game_map.matrix()
    if isinstance(game_map, GameMap):
        return sum(
            int(elem)
            for row in map_situation
            for elem in row
            if elem != "X" and elem not in players
        )

    return sum(int(elem) for row in map_situation for elem in row if elem not in players)


def update_map(
    game_map: GameMap,
    former_x: int,
    former_y: int,
    new_x: int,
    new_y: int,
    value: Literal["X", "P1", "P2", "P3"],
):

    game_map.update(former_x, former_y, "0")
    game_map.update(new_x, new_y, value)


def handle_movement(
    player: str,
    players: list[str],
    player_in_special_map: str,
    game_map: GameMap | SpecialGameMap,
    coin_db: dict[str, list[int]],
    map_situation: list[list],
    new_coordinates: tuple[int, int],
    former_coordinates: tuple[int, int],
    map_semaphore: BoundedSemaphore,
    special_map_semaphore: BoundedSemaphore,
    special_map_queue: Queue,
):
    x, y = new_coordinates[0], new_coordinates[1]
    former_x, former_y = former_coordinates[0], former_coordinates[1]

    # Se a posição escolhida pelo jogador for o mapa especial
    if map_situation[x][y] == "X":
        global special_game_map, special_map_is_empty

        # Bloco de espera ocupada para entrar no mapa especial
        # ========================================================
        if special_map_semaphore._value == 0:  # Se já tiver alguém no mapa especial
            next_player_to_special_map = handle_special_map_queue(
                special_map_queue, map_semaphore, special_map_semaphore, player
            )
            if special_map_is_empty:
                return  # apenas inicia uma nova jogada
        # ========================================================
        else:
            # Se não havia jogador no mapa especial então o próximo a entrar é o primeiro que solicitou
            next_player_to_special_map = player
            special_map_semaphore.acquire()

        # Jogador coletou a pontuação de onde estava, substitui por zero
        # e simula a entrada do player no mapa especial, "sumindo" com ele do mapa principal e deixando o mapa especial ("X") disponível para o restante dos players
        update_map(game_map, former_x, former_y, x, y, "X")

        map_semaphore.release()  # Já que o jogador vai entrar no mapa especial, libera o mapa principal para o restante dos players

        write_log(f"{next_player_to_special_map} ENTRANDO NO MAPA ESPECIAL")
        player_in_special_map = (
            next_player_to_special_map  # "Seta" o player que vai entrar no mapa especial)
        )
        play_special(
            player,
            players,
            coin_db,
            special_game_map,
            game_map,
            (x, y),
            map_semaphore,
            special_map_semaphore,
            special_map_queue,
            player_in_special_map,
        )

        # Devolve jogador que estava no mapa especial para o mapa principal logo na primeira posição que achar livre
        player_back_to_map(players, player_in_special_map, map_semaphore, game_map)
        special_map_semaphore.release()  # Libera o mapa especial após tempo de 10s
        write_log(f"{player_in_special_map} SAINDO DO MAPA ESPECIAL")
        sleep(0.5)
    else:
        if isinstance(game_map, GameMap):
            collect_coin(coin_db, (x, y), game_map, player)
        else:
            collect_coin(coin_db, (x, y), special_game_map, player)

        # Checando se a quantidade de pontos no mapa principal é igual a zero para finalizar o jogo.
        # =====================================================
        total_coins = get_total_coins(players, game_map)
        if (
            total_coins == 0
            and isinstance(game_map, GameMap)
            and not any("X" in row for row in map_situation)
        ):
            map_semaphore.release()
        # =====================================================
        else:
            # print(f"Player {player} got {sum(coin_db[player])} points.")

            # Jogador coletou a pontuação de onde estava e se move
            update_map(game_map, former_x, former_y, x, y, player)
            # Faz a comparação abaixo pois o player que está no mapa especial também usa a função
            # move_player, então o semáforo do mapa principal só será liberado se não for a thread
            # do player do mapa especial executando a função
            # ==================================
            if player != player_in_special_map:
                map_semaphore.release()
            # ==================================


def play(
    player: str,
    players: list[str],
    coin_db: dict[str, list],
    game_map: GameMap | SpecialGameMap,
    map_semaphore: BoundedSemaphore,
    special_map_semaphore: BoundedSemaphore,
    special_map_queue: Queue,
    player_in_special_map: str,
):

    sleep(1)

    if isinstance(game_map, GameMap):
        map_semaphore.acquire()

    show_map(game_map)

    map_situation = game_map.matrix()
    possible_moves, player_position = check_possible_moves(player, map_situation)

    player_choice = choice(KEYBOARD_OPTIONS).upper()

    x, y = player_position
    deltas = {
        "W": (-1, 0),  # Cima
        "A": (0, -1),  # Esquerda
        "S": (1, 0),  # Baixo
        "D": (0, 1),  # Direita
    }

    dx, dy = deltas[player_choice]

    new_player_position = (x + dx, y + dy)

    if new_player_position in possible_moves:
        handle_movement(
            player,
            players,
            player_in_special_map,
            game_map,
            coin_db,
            map_situation,
            new_player_position,
            player_position,
            map_semaphore,
            special_map_semaphore,
            special_map_queue,
        )
    else:
        if player != player_in_special_map:
            map_semaphore.release()


def remove_player_from_special_map(player: str, special_map_situation: list[list]) -> None:
    """
    Loop para achar a posição que o jogador parou no mapa especial após o tempo esgotado e trocar por zero, pois se parou em cima, coletou a pontuação daquela coordenada.
    """
    for i, j in product(range(len(special_map_situation)), range(len(special_map_situation))):
        if special_map_situation[i][j] == player:
            special_game_map.update(i, j, "0")
            break


def shut_special_map(game_map: GameMap, special_position: tuple[int, int]) -> None:
    global special_map_is_empty

    game_map.update(special_position[0], special_position[1], "0")
    special_map_is_empty = True


def empty_queue(special_map_queue: Queue) -> None:
    global queue_lock
    with queue_lock:
        if not special_map_queue.empty():
            write_log("================================================================")
            write_log("RECURSOS DO MAPA ESPECIAL ESGOTADOS, REMOVENDO JOGADORES DA FILA")
            while not special_map_queue.empty():
                removed_player = special_map_queue.get()
                write_log(f"{removed_player} REMOVIDO DA FILA.")
            write_log("================================================================")
            return
        write_log("===================================")
        write_log("RECURSOS DO MAPA ESPECIAL ESGOTADOS")
        write_log("===================================")


def play_special(
    player: str,
    players: list[str],
    coin_db: dict[str, list],
    special_game_map: SpecialGameMap,
    game_map: GameMap,
    special_position: tuple[int, int],
    map_semaphore: BoundedSemaphore,
    special_map_semaphore: BoundedSemaphore,
    special_map_queue: Queue,
    player_in_special_map: str,
):
    # Spota jogador no mapa especial
    spot_players([player], special_game_map)

    # Inicia a contagem de tempo no mapa especial
    start_time = time()
    while True:
        play(
            player,
            players,
            coin_db,
            special_game_map,
            map_semaphore,
            special_map_semaphore,
            special_map_queue,
            player_in_special_map,
        )

        # Se passar dos 10s, sai do loop
        if time() - start_time >= 10:
            break

        sleep(1)

    special_map_situation = special_game_map.matrix()
    remove_player_from_special_map(player, special_map_situation)

    #  Checa a pontuação total restante no mapa especial
    #  Se não houver mais pontos:
    #   - Fecha o mapa especial trocando a coordenada dele no mapa principal por zero;
    #   - Zera a fila de espera.
    #  ===============================================================================
    total_coins = get_total_coins(players, special_game_map)
    if total_coins == 0:
        shut_special_map(game_map, special_position)
        empty_queue(special_map_queue)
    #  ===============================================================================


def declare_champion(coin_db: dict[str, list]):
    print("\n")
    for k, v in coin_db.items():
        print(f"{k}: {sum(v)} pontos")
