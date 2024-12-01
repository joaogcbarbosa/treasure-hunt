from socket import socket, AF_INET, SOCK_STREAM
from ..utils.constants import HOST, PORT

def start_game():
    pass


def run_server(number_of_players: int) -> None:
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        accepted_connections = 0
        print("Running server...")
        while True:
            conn, addr = s.accept()
            if accepted_connections < number_of_players:
                print(f"Connection from {addr} accepted")
                accepted_connections += 1
                if accepted_connections == number_of_players:
                    start_game()
                print("Waiting for other players")
            else:
                print(f"Connection from {addr} refused")
                conn.close()
