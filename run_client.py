from threading import Thread, current_thread
from treasure_hunt.client.client import client
from treasure_hunt.models.map import GameMap
from treasure_hunt.utils.constants import SERVER_PORT, SERVER_HOST
from treasure_hunt.utils.checks import check_possible_moves
from treasure_hunt.utils.move import move_player
from treasure_hunt.utils.converters import string_to_matrix
import pickle

if __name__ == "__main__":
    def client_runner():
        thread_name = current_thread().name
        player = f"P{thread_name[7]}"  # posição 7 de thread name é o número da thread
        with client(SERVER_HOST, SERVER_PORT) as c:
            while True:

                data = c.recv(2048)  # Recebe os dados do servidor
                data = pickle.loads(data)
                map_situation: GameMap = data["game_map"]
                coin_db: dict[str, list] = data["coin_db"]

                print(map_situation.display())

                possible_moves, player_pos = check_possible_moves(
                    player, 
                    string_to_matrix(map_situation.display())
                )

                choice = input("Your turn: ").upper()
                map_situation = move_player(choice, player, possible_moves, player_pos, coin_db, map_situation)

                # Enviando mapa atualizado para servidor
                data = {
                    "game_map": map_situation,
                    "coin_db": coin_db,
                }
                data = pickle.dumps(data)
                c.sendall(data)  # Envia instância original do mapa e bancos

    client_thread = Thread(target=client_runner)
    client_thread.start()
