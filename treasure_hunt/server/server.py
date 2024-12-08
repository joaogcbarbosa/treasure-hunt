from socket import socket, AF_INET, SOCK_STREAM
from ..utils.constants import HOST, PORT
from ..models.map import GameMap
from random import randint
from .game import game


def server_runner(number_of_players: int) -> None:
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print()
        print("Running server...")
        print("Waiting for players to connect")
        print()
        accepted_connections = 0
        while True:
            conn, addr = s.accept()
            if accepted_connections < number_of_players:
                print(f"Connection from {addr} accepted")
                accepted_connections += 1
                if accepted_connections == number_of_players:
                    game(number_of_players, conn)
                else:
                    print("Waiting for other players")
            else:
                print(f"Connection from {addr} refused")
                conn.close()
