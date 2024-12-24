import pickle
from random import choice, random
from socket import socket, AF_INET, SOCK_STREAM
from threading import Lock, Thread
from time import sleep

from treasure_hunt.client.client import client
from treasure_hunt.models.map import GameMap
from treasure_hunt.utils.checks import check_number_of_players, check_possible_moves
from treasure_hunt.utils.converters import string_to_matrix
from treasure_hunt.utils.move import move_player
from treasure_hunt.utils.templates import number_of_players, treasure_hunt_title
from ..utils.constants import HOST, PORT, SERVER_HOST, SERVER_PORT
from .game import spot_players
from .game_map import game_map

coin_db: dict[str, list] = {}
player_counter: int = 0
resource_lock: Lock = Lock()


def init_coin_db(number_of_players: int) -> dict[str, list]:
    return {f"P{i}": [] for i in range(1, number_of_players + 1)}


def client_runner(player: str):
    with client(SERVER_HOST, SERVER_PORT) as c:
        while True:
            try:
                with resource_lock:
                    data = c.recv(2048) 
                    data = pickle.loads(data)
                    map_situation: GameMap = data["game_map"]
                    coin_db: dict[str, list] = data["coin_db"]

                    print(map_situation.display())
                    possible_moves, player_pos = check_possible_moves(
                        player, 
                        string_to_matrix(map_situation.display())
                    )

                    # choice = input(f"{player} turn: ").upper()
                    print(f"{player} turn:", end=" ")
                    player_choice = choice(["w", "a", "s", "d"]).upper()
                    sleep(random())
                    move_player(player_choice, player, possible_moves, player_pos, coin_db, map_situation)

                    data = {
                        "game_map": map_situation,
                        "coin_db": coin_db,
                    }
                    data = pickle.dumps(data)
                    c.sendall(data)

            except Exception as e:
                print(f"Erro com o client: {e}")
                break


def server_runner(number_of_players: int):
    global coin_db

    coin_db = init_coin_db(number_of_players)
    accepted_connections: int = 0
    player_counter: int = 0
    connections: list[socket] = []

    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Running server...")
        while True:
            if accepted_connections < number_of_players:
                conn, addr = s.accept()
                connections.append(conn)
                print(f"Connection from {addr} accepted")
                accepted_connections += 1
                player_counter += 1
                conn.send(f"{player_counter}".encode())
                print(f"{accepted_connections}/{number_of_players}")
                if accepted_connections == number_of_players:
                    print("Initializing map.\n")
                    spot_players(number_of_players)
            else:
                data = {
                "game_map": game_map,
                "coin_db": coin_db,
                }
                data = pickle.dumps(data)
                map_situation = None
                db_situation = None
                while not (isinstance(map_situation, GameMap) and isinstance(db_situation, dict)):
                    conn.sendall(data)  # Envia a instância original do mapa
                    data_from_client = pickle.loads(conn.recv(2048))
                    map_situation = data_from_client["game_map"]  # Carrega mapa alterado pelo cliente
                    db_situation = data_from_client["coin_db"]  # Carrega banco alterado pelo cliente
                coin_db.update(db_situation)


if __name__ == "__main__":
    # Terminal Template
    treasure_hunt_title()  # TODO: deve aparecer para o player
    number_of_players()
    # =================
    nro_players = check_number_of_players()
    server_runner(nro_players)

    players = [Thread(target=client_runner, args=(f"P{str(i)}"),) for i in range(1, nro_players + 1)]

    for p in players:
        p.start()
