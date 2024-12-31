from queue import Queue
from random import choice, randint
from threading import BoundedSemaphore, Event, Lock
from time import sleep, time
from typing import Literal

from ..models.map import GameMap, SpecialGameMap
from ..utils.checks import check_possible_moves
from ..utils.constants import KEYBOARD_OPTIONS
from ..utils.converters import string_to_matrix

special_game_map = SpecialGameMap()
queue_lock: Lock = Lock()
check_semaphore = BoundedSemaphore()


def collect_coin(
    coin_db: dict[str, list],
    coin_position: tuple[int, int],
    game_map: GameMap | SpecialGameMap,
    player: str,
):
    map_situation = string_to_matrix(game_map.display())
    coin_db[player].append(int(map_situation[coin_position[0]][coin_position[1]]))


def player_back_to_map(
    map_semaphore: BoundedSemaphore,
    map_situation: list[list],
    game_map: GameMap,
    player_in_special_map: str,
):
    map_semaphore.acquire()
    _break = False
    for i in range(len(map_situation)):
        for j in range(len(map_situation)):
            if map_situation[i][j] not in ("P1", "P2", "P3"):
                game_map.update(i, j, player_in_special_map)
                _break = True
                break
        if _break:
            break
    map_semaphore.release()


def handle_special_map_queue(
    special_map_queue: Queue, 
    map_semaphore: BoundedSemaphore, 
    special_map_semaphore: BoundedSemaphore,
    player: str, 
) -> str:
    global queue_lock
    next_to_special_map: str = ""  # player
    with queue_lock:
        special_map_queue.put(player)  # Põe jogador na fila para o mapa especial
        map_semaphore.release()  # Jogadores que entram para a fila do mapa especial ficam em espera ocupada, então param de alterar o mapa principal
    while True:
        check_semaphore.acquire()  # Semáforo para uma thread de cada vez checar se o semáforo do mapa especial foi liberado
        if special_map_semaphore._value != 0:
            next_to_special_map = special_map_queue.get() # Se o semáforo do mapa especial foi liberado então o próximo da fila é resgatado
            map_semaphore.acquire()  # Faz acquire para o mapa principal para realizar o movimento de entrada no mapa especial
            special_map_semaphore.acquire()
            check_semaphore.release()
            break
        check_semaphore.release()
    return next_to_special_map


def get_total_coins(map_situation: list[list]):
    return sum(
        int(elem)
        for row in map_situation
        for elem in row
        if elem != "X" and elem not in ("P1", "P2", "P3")
    )


def update_map(
    game_map: GameMap | SpecialGameMap, 
    former_x: int, 
    former_y: int, 
    new_x: int, 
    new_y: int, 
    value: str,  # "X" or player
):

    game_map.update(former_x, former_y, "0")
    game_map.update(new_x, new_y, value)


def handle_movement(
    player: str,
    player_in_special_map: str,
    game_map: GameMap | SpecialGameMap,
    coin_db: dict[str, list[int]],
    map_situation: list[list],
    new_coordinates: tuple[int, int],
    former_coordinates: tuple[int, int],
    map_semaphore: BoundedSemaphore,
    special_map_semaphore: BoundedSemaphore,
    special_map_queue: Queue,
    event: Event,
):
    x, y = new_coordinates[0], new_coordinates[1]
    former_x, former_y = former_coordinates[0], former_coordinates[1]

    # Se a posição escolhida pelo jogador for o mapa especial
    if map_situation[x][y] == "X":
        global special_game_map

        # Bloco de espera ocupada para entrar no mapa especial
        # ========================================================
        if special_map_semaphore._value == 0:  # Se já tiver alguém no mapa especial
            next_to_special_map = handle_special_map_queue(special_map_queue,  map_semaphore, special_map_semaphore, player)
        # ========================================================
        else:
            # Se não havia jogador no mapa especial então o próximo a entrar é o primeiro que solicitou
            next_to_special_map = player
            special_map_semaphore.acquire()

        # Jogador coletou a pontuação de onde estava, substitui por zero
        # e simula a entrada do player no mapa especial, "sumindo" com ele do mapa principal e deixando o mapa especial ("X") disponível para o restante dos players
        update_map(game_map, former_x, former_y, x, y, "X")

        map_semaphore.release()  # Já que o jogador vai entrar no mapa especial, libera o mapa principal para o restante dos players

        player_in_special_map = next_to_special_map  # "Seta" o player que vai entrar no mapa especial)
        play_special(
            player,
            coin_db,
            special_game_map,
            game_map,
            (x, y),
            event,
            map_semaphore,
            special_map_semaphore,
            special_map_queue,
            player_in_special_map,
        )

        # Devolve jogador que estava no mapa especial para o mapa principal logo na primeira posição que achar livre
        # ======================================================
        player_back_to_map(map_semaphore, map_situation, game_map, player_in_special_map)
        # ======================================================
        special_map_semaphore.release()  # Libera o mapa especial após tempo de 10s
    else:
        collect_coin(coin_db, (x, y), game_map, player)

        # Checando se a quantidade de pontos no mapa principal é igual a zero para finalizar o jogo.
        # =====================================================
        total_coins = get_total_coins(map_situation)
        if (
            total_coins == 0
            and isinstance(game_map, GameMap)
            and not any("X" in row for row in map_situation)
        ):
            declare_champion(coin_db)
            event.set()
        # =====================================================
        else:
            print(f"Player {player} got {sum(coin_db[player])} points.")

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
    choice: Literal["W", "A", "S", "D"],
    player: str,
    possible_moves: list[tuple[int]],
    player_position: tuple[int, int],
    coin_db: dict[str, list],
    game_map: GameMap | SpecialGameMap,
    event: Event,
    map_semaphore: BoundedSemaphore,
    special_map_semaphore: BoundedSemaphore,
    special_map_queue: Queue,
    player_in_special_map: str,
):
    x, y = player_position

    deltas = {
        "W": (-1, 0),  # Cima
        "A": (0, -1),  # Esquerda
        "S": (1, 0),  # Baixo
        "D": (0, 1),  # Direita
    }

    dx, dy = deltas[choice]

    new_player_position = (x + dx, y + dy)

    if new_player_position in possible_moves:
        map_situation = string_to_matrix(game_map.display())
        handle_movement(player, player_in_special_map, game_map, coin_db, map_situation, new_player_position, player_position, map_semaphore, special_map_semaphore, special_map_queue, event)
    else:
        print("Could not move.")
        if player != player_in_special_map:
            map_semaphore.release()


def play_special(
    player: str,
    coin_db: dict[str, list],
    special_game_map: SpecialGameMap,
    game_map: GameMap,
    special_position: tuple[int, int],
    event: Event,
    map_semaphore: BoundedSemaphore,
    special_map_semaphore: BoundedSemaphore,
    special_map_queue: Queue,
    player_in_special_map: str,
) -> bool:
    # Spota jogador no mapa especial de acordo com os limites
    height_bound, width_bound = special_game_map.bounds()
    height, width = randint(0, height_bound), randint(0, width_bound)
    special_game_map.update(height, width, player)
    # Inicia a contagem de tempo no mapa especial
    start_time = time()
    while True:
        print(special_game_map.display())
        possible_moves, player_pos = check_possible_moves(
            player, string_to_matrix(special_game_map.display())
        )
        print(f"{player} turn:", end=" ")
        player_choice = choice(KEYBOARD_OPTIONS).upper()
        # player_choice = input().upper()
        play(
            player_choice,
            player,
            possible_moves,
            player_pos,
            coin_db,
            special_game_map,
            event,
            map_semaphore,
            special_map_semaphore,
            special_map_queue,
            player_in_special_map,
        )

        # Se passar dos 10s, sai do loop
        if time() - start_time >= 10:
            break

        sleep(1)

    #  Loop para achar a posição que o jogador parou no mapa especial após o tempo esgotado e trocar por zero, pois se parou em cima, coletou a pontuação daquela coordenada
    #  ==================================================================
    special_map_situation = string_to_matrix(special_game_map.display())
    for i in range(len(special_map_situation)):
        for j in range(len(special_map_situation)):
            if special_map_situation[i][j] == player:
                special_game_map.update(i, j, "0")
    #  ==================================================================

    #  Checa a pontuação total restante no mapa especial. Se não houver mais pontos, 
    #  fecha o mapa especial trocando a coordenada dele no mapa principal por zero e zera a fila de espera
    #  =============================================================================================
    total_coins = sum(
        int(elem) for row in special_map_situation for elem in row if elem not in ("P1", "P2", "P3")
    )
    if total_coins == 0:
        game_map.update(special_position[0], special_position[1], "0")

        global queue_lock
        with queue_lock:
            #  Remove todos jogadores da fila de espera para o mapa especial já que o mesmo não tem mais pontos para serem coletados
            while not special_map_queue.empty():
                removed_player = special_map_queue.get()
                print(f"Player {removed_player} removed from queue.")
    #  =============================================================================================


def declare_champion(coin_db: dict[str, list]):
    print("\n")
    for k, v in coin_db.items():
        print(f"{k}: {sum(v)} pontos")
