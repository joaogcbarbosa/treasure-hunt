from socket import socket
from time import sleep
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


def game(number_of_players: int, conn: socket):
    global game_map, rnd, occupied_spots
    print("Initializing map.\n")
    sleep(2)
    while True:
        if rnd == 0:
            game_map = spot_players(number_of_players, game_map)
            print(game_map.display())
        else:
            mensagem = game_map.display()
            conn.sendall(mensagem.encode('utf-8'))
        rnd += 1
        sleep(5)
