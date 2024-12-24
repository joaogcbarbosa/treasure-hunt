from random import choice
from socket import socket, AF_INET, SOCK_STREAM
from threading import Lock, Thread
from time import sleep

from treasure_hunt.client.client import client
from treasure_hunt.utils.checks import check_number_of_players, check_possible_moves
from treasure_hunt.utils.converters import string_to_matrix
from treasure_hunt.utils.move import move_player
from treasure_hunt.utils.templates import number_of_players, treasure_hunt_title
from treasure_hunt.utils.constants import HOST, PORT, SERVER_HOST, SERVER_PORT
from treasure_hunt.server.game import spot_players
from treasure_hunt.server.game_map import game_map

coin_db: dict[str, list] = {}
player_counter: int = 0
lock = Lock()

def init_coin_db(number_of_players: int) -> dict[str, list]:
    return {f"P{i}": [] for i in range(1, number_of_players + 1)}


def client_runner(player: str):
    global game_map, coin_db, lock
    with client(SERVER_HOST, SERVER_PORT):
        sleep(3)  # Tempo para deixar o servidor plotar os players conectados no mapa
        while True:
            try:
                # Região crítica, pois altera a situação do mapa do jogo e do banco de coins
                # ==================================================
                with lock:
                    print(game_map.display())
                    possible_moves, player_pos = check_possible_moves(
                        player, 
                        string_to_matrix(game_map.display())
                    )
                    print(f"{player} turn:", end=" ")
                    player_choice = choice(["w", "a", "s", "d"]).upper()
                    # player_choice = input().upper()
                    move_player(player_choice, player, possible_moves, player_pos, coin_db, game_map)
                # ==================================================
                sleep(1)
            except Exception as e:
                print(f"Erro com o client: {e}")
                break


def server_runner(number_of_players: int):
    global coin_db

    coin_db = init_coin_db(number_of_players)
    accepted_connections: int = 0

    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Running server...")
        while True:
            if accepted_connections < number_of_players:
                _, addr = s.accept()
                print(f"Connection from {addr} accepted")
                accepted_connections += 1
                print(f"{accepted_connections}/{number_of_players}")
                if accepted_connections == number_of_players:
                    print("Initializing map.\n")
                    spot_players(number_of_players)


if __name__ == "__main__":
    # Terminal Template
    treasure_hunt_title()
    number_of_players()
    # =================

    nro_players = check_number_of_players()

    server = Thread(target=server_runner, args=(nro_players,))
    players = [Thread(target=client_runner, args=(f"P{str(i)}",)) for i in range(1, nro_players + 1)]

    server.start()
    sleep(2)  # tempo para o servidor iniciar
    for p in players:
        p.start()
