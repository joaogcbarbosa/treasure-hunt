from queue import Queue
from random import choice, randint
from socket import AF_INET, SOCK_STREAM, socket
from threading import BoundedSemaphore, Event, Thread
from time import sleep

from treasure_hunt.client.client import client
from treasure_hunt.models.map import GameMap
from treasure_hunt.server.game import spot_players
from treasure_hunt.utils.checks import check_number_of_players, check_possible_moves
from treasure_hunt.utils.constants import HOST, KEYBOARD_OPTIONS, PORT, SERVER_HOST, SERVER_PORT, MAX_PLAYERS
from treasure_hunt.utils.converters import string_to_matrix
from treasure_hunt.utils.move import play
from treasure_hunt.utils.templates import number_of_players, treasure_hunt_title

game_map: GameMap
coin_db: dict[str, list]
map_semaphore = BoundedSemaphore()
special_map_semaphore = BoundedSemaphore()
special_map_queue = Queue(maxsize=MAX_PLAYERS - 1)
stop_event = Event()
player_in_special_map: str = ""


def init_coin_db(number_of_players: int) -> dict[str, list]:
    return {f"P{i}": [] for i in range(1, number_of_players + 1)}


def client_runner(player: str):
    global game_map, coin_db, map_semaphore, special_map_semaphore, special_map_queue, stop_event, player_in_special_map
    with client(SERVER_HOST, SERVER_PORT):
        sleep(5)  # Tempo para deixar o servidor plotar os players conectados no mapa
        while not stop_event.is_set():
            try:
                # Região crítica, pois altera a situação do mapa do jogo e do banco de coins.
                # Não há semáforo para o banco de coins pois a proteção da região crítica
                # pelo semáforo do mapa já protege o banco.
                # ==================================================
                sleep(1)
                map_semaphore.acquire()
                print(game_map.display())
                possible_moves, player_pos = check_possible_moves(
                    player, string_to_matrix(game_map.display())
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
                    game_map,
                    stop_event,
                    map_semaphore,
                    special_map_semaphore,
                    special_map_queue,
                    player_in_special_map,
                )
                # ==================================================
            except Exception as e:
                print(player)
                print(f"Erro com o client: {e}")
                break


def server_runner(number_of_players: int):
    global coin_db, game_map

    game_map = GameMap()
    coin_db = init_coin_db(number_of_players)
    accepted_connections: int = 0

    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Running server...")
        while not stop_event.is_set():
            if accepted_connections < number_of_players:
                _, addr = s.accept()
                print(f"Connection from {addr} accepted")
                accepted_connections += 1
                print(f"{accepted_connections}/{number_of_players}")
                if accepted_connections == number_of_players:
                    sleep(0.5)
                    print("Initializing map.\n")
                    spot_players(number_of_players, game_map)
                    sleep(1)


if __name__ == "__main__":
    # Terminal Template
    treasure_hunt_title()
    number_of_players()
    # =================

    nro_players = check_number_of_players()

    server = Thread(target=server_runner, args=(nro_players,))
    players = [
        Thread(target=client_runner, args=(f"P{str(i)}",)) for i in range(1, nro_players + 1)
    ]

    server.start()
    sleep(3)  # tempo para o servidor iniciar
    for p in players:
        p.start()
        sleep(1)  # para simular entrada de cada vez de players no servidor

    for p in players:
        p.join()

    server.join()
