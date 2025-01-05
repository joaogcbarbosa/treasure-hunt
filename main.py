from queue import Queue
from socket import AF_INET, SOCK_STREAM, socket
from threading import BoundedSemaphore, Thread, Event
from time import sleep

from treasure_hunt.client.client import client
from treasure_hunt.map import GameMap
from treasure_hunt.player_spotter import spot_players
from treasure_hunt.utils.checks import check_number_of_players
from treasure_hunt.utils.constants import HOST, MAX_PLAYERS, PORT, SERVER_HOST, SERVER_PORT
from treasure_hunt.utils.play import declare_champion, get_total_coins, play
from treasure_hunt.utils.templates import number_of_players, treasure_hunt_title

game_map: GameMap
coin_db: dict[str, list]
map_semaphore = BoundedSemaphore()
special_map_semaphore = BoundedSemaphore()
special_map_queue = Queue(maxsize=MAX_PLAYERS - 1)
player_in_special_map: str = ""
finish_game: Event = Event()


def init_coin_db(number_of_players: int) -> dict[str, list[int]]:
    """
    Inícia um banco de dados simulado com a seguinte estrutura de exemplo:
    coin_db = {
        "P1": [2, 7, 8, 5],
        "P2": [3, 7],
    }
    Sendo a key do dicionário o player e o value uma lista com os pontos coletados.
    """
    return {f"P{i}": [] for i in range(1, number_of_players + 1)}


def client_runner(player: str, players: list[str]):
    """
    Duas ou três threads que ficam em looping infinito executando a função "play" 
    (se movendo pelos mapas e coletando pontos) até que a condição de parada seja verdadeira 
    (ambos mapas com nenhum ponto restante para ser coletado).
    """
    global game_map, coin_db, map_semaphore, special_map_semaphore, special_map_queue, player_in_special_map, finish_game
    with client(SERVER_HOST, SERVER_PORT):
        sleep(5)  # Tempo para deixar o servidor plotar os players conectados no mapa
        while True:
            try:
                play(
                    player,
                    players,
                    player_in_special_map,
                    coin_db,
                    game_map,
                    map_semaphore,
                    special_map_semaphore,
                    special_map_queue,
                    finish_game,
                )

                if finish_game.is_set():
                    break

            except Exception as e:
                print(f"{player} - Client error: {e}")
                break


def server_runner(clients: list[str]):
    """
    Servidor é inicializado com host e porta. 
    Fica escutando e aceitando as solicitações de conexão de novos clientes. 
    Quando o número de conexões passa a ser igual ao número de players informados para a partida, 
    o servidor "spawna" os jogadores no mapa principal e aguarda em looping infinito até a condição da flag de parada ser verdadeira, 
    momento de encerramento da thread do servidor.
    """
    global game_map, coin_db, finish_game

    number_of_players: int = len(clients)
    connections: int = 0

    game_map = GameMap()
    coin_db = init_coin_db(number_of_players)


    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Running server...")
        while True:
            try:
                if finish_game.is_set():
                    sleep(2)  # Deixando as Threads dos players terminarem antes do servidor
                    print("Shutting down server")
                    break
                if connections < number_of_players:
                    """
                    Enquanto o número de conexões for menor que o número de players informados para a partida
                    o servidor continua recebendo conexões.
                    """
                    _, addr = s.accept()
                    print(f"Connection from {addr} accepted")
                    connections += 1
                    print(f"{connections}/{number_of_players}")
                    if connections == number_of_players:
                        """
                        No momento que o número de conexões é igual ao número de players informados para a partida
                        o servidor "spawna" os players no mapa.
                        """
                        sleep(1)
                        print("Initializing map.\n")
                        spot_players(clients, game_map)
                        sleep(1)
            except Exception as e:
                print(f"Server error: {e}")
                break


if __name__ == "__main__":
    treasure_hunt_title()  # Título
    number_of_players()  # Escolher quantidade de jogadores

    nro_players = check_number_of_players()  # Guarda a quantidade de jogadores da partida
    clients = [f"P{i}" for i in range(1, nro_players + 1)]  # Lista de players. Ex: ["P1", "P2"]

    server = Thread(target=server_runner, args=(clients,))
    players = [
        Thread(target=client_runner, args=(f"P{str(i)}", clients))
        for i in range(1, nro_players + 1)
    ]  # Cada thread envia como argumento para client_runner o jogador e a lista de jogadores

    server.start()
    sleep(2)  # Tempo para o servidor iniciar
    for p in players:
        p.start()
        sleep(1)  # Simulando entrada de cada vez de players no servidor

    for p in players:
        p.join()
                      # Encerramento das threads dos jogadores e do servidor
    server.join()

    declare_champion(coin_db)  # Printa no terminal a pontuação final de cada jogador
