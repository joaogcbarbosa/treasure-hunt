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
