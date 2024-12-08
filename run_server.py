from multiprocessing.pool import ThreadPool
from threading import Thread
from treasure_hunt.utils.templates import treasure_hunt_title, number_of_players
from treasure_hunt.utils.checks import check_number_of_players, check_possible_moves
from treasure_hunt.server.server import server_runner
from treasure_hunt.client.client import client
from treasure_hunt.utils.constants import SERVER_HOST, SERVER_PORT
from treasure_hunt.server.game_map import game_map
from treasure_hunt.utils.move import move_player
from treasure_hunt.utils.converters import string_to_matrix

import pickle

def client_runner():
    with client(SERVER_HOST, SERVER_PORT) as c:
        while True:

            data = c.recv(1024)
            if not data:
                print("Server has reached its limit of connections.")
                break

            data = c.recv(1024)
            data = pickle.loads(data)
            map_situation = string_to_matrix(data["map_situation"].display())
            your_turn_sentence = data["your_turn_sentence"]
            player = data["player"]

            print(game_map.display())
            possible_moves, player_pos = check_possible_moves(player, map_situation)
            choice = input(your_turn_sentence)
            move_player(choice, possible_moves, player_pos, game_map)
            print(game_map.display())


def main():
    # Terminal Template
    treasure_hunt_title()  # TODO: deve aparecer para o player
    number_of_players()
    # =================
    nro_players = check_number_of_players()
    server_thread = Thread(target=server_runner, args=(nro_players,))
    server_thread.start()  # Inicia servidor, que fica escutando e esperando players conectarem


if __name__ == "__main__":
    main()
