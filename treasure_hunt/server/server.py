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
            if accepted_connections < number_of_players:
                conn, addr = s.accept()
                print(f"Connection from {addr} accepted")
                accepted_connections += 1
                print("Waiting for other players")
            elif accepted_connections == number_of_players:
                game(number_of_players, conn) 
            else:
                print(f"Connection from {addr} refused")
                conn.close()
