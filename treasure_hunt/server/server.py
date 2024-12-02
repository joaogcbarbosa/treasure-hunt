from socket import socket, AF_INET, SOCK_STREAM
from ..utils.constants import HOST, PORT
from ..models.map import GameMap
from random import randint

game_map = GameMap()

def spot_players(number_of_players: int, game_map: GameMap) -> GameMap:
    occupied_spots = []
    for i in range(1, number_of_players + 1):
        height_bound, width_bound = game_map.bounds()
        height, width = randint(0, height_bound), randint(0, width_bound)
        while (height, width) in occupied_spots:
            height, width = randint(0, height_bound), randint(0, width_bound)
        game_map.update(height, width, f"P{i}")
        occupied_spots.append((height, width))
    return game_map


def game(number_of_players: int):
    global game_map
    game_map = spot_players(number_of_players, game_map)
    game_map.display()


def run_server(number_of_players: int) -> None:
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        accepted_connections = 0
        print("Running server...")
        while True:
            conn, addr = s.accept()
            if accepted_connections < number_of_players:
                print(f"Connection from {addr} accepted")
                accepted_connections += 1
                if accepted_connections == number_of_players:
                    game(number_of_players)
                print("Waiting for other players")
            else:
                print(f"Connection from {addr} refused")
                conn.close()
