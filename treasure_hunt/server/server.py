from socket import socket, AF_INET, SOCK_STREAM
from ..utils.constants import HOST, PORT
from ..models.map import GameMap
from random import randint

game_map = GameMap()
rnd = 0
occupied_spots = []

def move_player():
    global occupied_spots
    # TODO: continue from here


def spot_players(number_of_players: int, game_map: GameMap) -> GameMap:
    global occupied_spots
    for i in range(1, number_of_players + 1):
        height_bound, width_bound = game_map.bounds()
        height, width = randint(0, height_bound), randint(0, width_bound)
        player = f"P{i}"
        while (height, width) in occupied_spots:
            height, width = randint(0, height_bound), randint(0, width_bound)
        game_map.update(height, width, player)
        occupied_spots.append((height, width, player))
    return game_map


def game(number_of_players: int):
    global game_map, rnd, occupied_spots
    if rnd == 0:
        game_map = spot_players(number_of_players, game_map)
    else:
        game_map = move_player(game_map, occupied_spots)
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
                    while True:
                        game(number_of_players)
                else:
                    print("Waiting for other players")
            else:
                print(f"Connection from {addr} refused")
                conn.close()
