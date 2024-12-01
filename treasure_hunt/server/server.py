from socket import socket, AF_INET, SOCK_STREAM
from ..utils.constants import HOST, PORT

def run_server(number_of_players: int):
    server_socket = socket(family=AF_INET, type=SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(number_of_players)

    conn, addr = server_socket.accept()
    print(f"Server initialized on {addr}")

    while True:
        msg = conn.recv(1024)
        if not msg:
            break
        decoded_msg = msg.decode("utf-8")
        print(decoded_msg)

    conn.close()
