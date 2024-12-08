from time import sleep
from treasure_hunt.client.client import client
from treasure_hunt.models.map import GameMap
from treasure_hunt.utils.constants import SERVER_PORT, SERVER_HOST
from treasure_hunt.utils.checks import check_possible_moves
from treasure_hunt.utils.move import move_player
from treasure_hunt.server.game_map import game_map
from treasure_hunt.utils.converters import string_to_matrix
import pickle

if __name__ == "__main__":
    with client(SERVER_HOST, SERVER_PORT) as c:
        while True:


            data = c.recv(2048)  # Recebe os dados do servidor
            data = pickle.loads(data)
            map_situation: GameMap = data["game_map"]
            player: str = data["player"]

            print(map_situation.display())

            possible_moves, player_pos = check_possible_moves(
                player, 
                string_to_matrix(map_situation.display())
            )

            choice = input("Your turn: ").upper()
            map_situation = move_player(choice, possible_moves, player_pos, map_situation)

            # Enviando mapa atualizado para servidor
            data = {
                "game_map": map_situation,
            }
            data = pickle.dumps(data)
            c.sendall(data)  # Envia instância original do mapa
