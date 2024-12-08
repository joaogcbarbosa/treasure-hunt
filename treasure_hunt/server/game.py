from socket import socket
from time import sleep
from ..models.map import GameMap
from .game_map import game_map
from random import randint
import pickle

rnd = 0
occupied_spots = []

def spot_players(number_of_players: int, game_map: GameMap) -> None:
    global occupied_spots
    for i in range(1, number_of_players + 1):
        height_bound, width_bound = game_map.bounds()
        height, width = randint(0, height_bound), randint(0, width_bound)
        player = f"P{i}"
        while (height, width) in occupied_spots:
            height, width = randint(0, height_bound), randint(0, width_bound)
        game_map.update(height, width, player)
        occupied_spots.append((height, width, player))


def game(number_of_players: int, coin_db: dict[str, list], conn: socket):
    global rnd
    if rnd == 0:
        print("Initializing map.\n")
        sleep(2)
        spot_players(number_of_players, game_map)  # Altera instância original do mapa
        rnd += 1

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
