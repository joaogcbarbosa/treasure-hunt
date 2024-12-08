from treasure_hunt.client.client import client
from treasure_hunt.utils.constants import SERVER_PORT, SERVER_HOST
from treasure_hunt.utils.checks import check_possible_moves
from treasure_hunt.utils.move import move_player
from treasure_hunt.server.game_map import game_map
from treasure_hunt.utils.converters import string_to_matrix
import pickle

if __name__ == "__main__":
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
