import pickle
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import sleep

from run_client import handle_client
from treasure_hunt.models.map import GameMap
from ..utils.constants import HOST, PORT
from .game import spot_players
from .game_map import game_map

coin_db: dict[str, list] = {}
player_counter: int = 0


def init_coin_db(number_of_players: int) -> dict[str, list]:
    return {f"P{i}": [] for i in range(1, number_of_players + 1)}


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
                for conn in connections:
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
