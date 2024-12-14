from threading import Thread, current_thread, Lock
from time import sleep
from treasure_hunt.server.game_map import game_map
from treasure_hunt.client.client import client
from treasure_hunt.models.map import GameMap
from treasure_hunt.utils.constants import SERVER_PORT, SERVER_HOST
from treasure_hunt.utils.checks import check_possible_moves
from treasure_hunt.utils.move import move_player
from treasure_hunt.utils.converters import string_to_matrix
import pickle
from random import choice

resource_lock: Lock = Lock()

def handle_client():

    with client(SERVER_HOST, SERVER_PORT) as c:
        data = c.recv(1024).decode()
        player = f"P{str(data)}"
        while True:
            try:
                with resource_lock:
                    data = c.recv(2048) 
                    data = pickle.loads(data)
                    map_situation: GameMap = data["game_map"]
                    coin_db: dict[str, list] = data["coin_db"]

                    print(map_situation.display())
                    possible_moves, player_pos = check_possible_moves(
                        player, 
                        string_to_matrix(map_situation.display())
                    )

                    # choice = input(f"{player} turn: ").upper()
                    print(f"{player} turn:", end=" ")
                    player_choice = choice(["w", "a", "s", "d"]).upper()
                    sleep(2)
                    move_player(player_choice, player, possible_moves, player_pos, coin_db, map_situation)

                    data = {
                        "game_map": map_situation,
                        "coin_db": coin_db,
                    }
                    data = pickle.dumps(data)
                    c.sendall(data)

            except Exception as e:
                print(f"Erro com o client: {e}")
                break


if __name__ == "__main__":
    thread = Thread(target=handle_client)
    thread.start()

