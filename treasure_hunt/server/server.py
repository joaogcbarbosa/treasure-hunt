from socket import socket, AF_INET, SOCK_STREAM
from ..utils.constants import HOST, PORT
from .game import game

def init_coin_db(number_of_players: int) -> dict[str, list]:
    return {f"P{i}": [] for i in range(1, number_of_players + 1)}


def server_runner(number_of_players: int) -> None:
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print()
        print("Running server...")
        print("Waiting for players to connect")
        print()
        accepted_connections = 0
        coin_db = init_coin_db(number_of_players)

        while True:
            if accepted_connections < number_of_players:
                conn, addr = s.accept()
                print(f"Connection from {addr} accepted")
                accepted_connections += 1
                print("Waiting for other players")
            elif accepted_connections == number_of_players:
                game(number_of_players, coin_db, conn) 
            else:
                print(f"Connection from {addr} refused")
                conn.close()
