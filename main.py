from queue import Queue
from socket import AF_INET, SOCK_STREAM, socket
from threading import BoundedSemaphore, Thread
from time import sleep

from treasure_hunt.client.client import client
from treasure_hunt.models.map import GameMap
from treasure_hunt.server.game import spot_players
from treasure_hunt.utils.checks import check_number_of_players
from treasure_hunt.utils.constants import HOST, PORT, SERVER_HOST, SERVER_PORT, MAX_PLAYERS
from treasure_hunt.utils.move import play, declare_champion, get_total_coins
from treasure_hunt.utils.templates import number_of_players, treasure_hunt_title


game_map: GameMap
coin_db: dict[str, list]
map_semaphore = BoundedSemaphore()
special_map_semaphore = BoundedSemaphore()
special_map_queue = Queue(maxsize=MAX_PLAYERS - 1)
player_in_special_map: str = ""
connections: int


def init_coin_db(number_of_players: int) -> dict[str, list]:
    return {f"P{i}": [] for i in range(1, number_of_players + 1)}


def client_runner(player: str, players: list[str]):
    global game_map, coin_db, map_semaphore, special_map_semaphore, special_map_queue, player_in_special_map, connections
    with client(SERVER_HOST, SERVER_PORT):
        sleep(5)  # Tempo para deixar o servidor plotar os players conectados no mapa
        while True:
            try:
                # Região crítica, pois altera a situação do mapa do jogo e do banco de coins.
                # Não há semáforo para o banco de coins pois a proteção da região crítica
                # pelo semáforo do mapa já protege o banco.
                # ==================================================
                play(
                    player,
                    players,
                    coin_db,
                    game_map,
                    map_semaphore,
                    special_map_semaphore,
                    special_map_queue,
                    player_in_special_map,
                )
                map_situation = game_map.matrix()
                total_coins = get_total_coins(players, map_situation)
                if total_coins == 0 and isinstance(game_map, GameMap) and not any("X" in row for row in map_situation):
                    print(f"Disconnecting {player}")
                    connections = -1
                    break
                # ==================================================
            except Exception as e:
                print(player)
                print(f"Erro com o client: {e}")
                break


def server_runner(clients: list[str]):
    global coin_db, game_map, connections

    game_map = GameMap()
    number_of_players = len(clients)
    coin_db = init_coin_db(number_of_players)
    connections = 0

    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Running server...")
        while True:
            if connections == -1:
                sleep(2)  # Deixando as Threads dos players terminarem antes do servidor 
                print("Shutting down server")
                break
            if connections < number_of_players:
                _, addr = s.accept()
                print(f"Connection from {addr} accepted")
                connections += 1
                print(f"{connections}/{number_of_players}")
                if connections == number_of_players:
                    sleep(1)
                    print("Initializing map.\n")
                    spot_players(clients, game_map)
                    sleep(1)


if __name__ == "__main__":
    # Terminal Template
    treasure_hunt_title()
    number_of_players()
    # =================

    nro_players = check_number_of_players()
    clients = [f"P{i}" for i in range(1, nro_players + 1)]

    server = Thread(target=server_runner, args=(clients,))
    players = [
        Thread(target=client_runner, args=(f"P{str(i)}", clients)) for i in range(1, nro_players + 1)
    ]

    server.start()
    sleep(2)  # Tempo para o servidor iniciar
    for p in players:
        p.start()
        sleep(1)  # Simulando entrada de cada vez de players no servidor

    for p in players:
        p.join()

    server.join()

    declare_champion(coin_db)
