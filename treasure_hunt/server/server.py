from socket import socket, AF_INET, SOCK_STREAM
from ..utils.constants import MAX_PLAYERS, HOST, PORT

def run_server():
    server_socket = socket(family=AF_INET, type=SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_PLAYERS)

    conn, addr = server_socket.accept()
    print(f"Server initialized on {addr}")

    while True:
        msg = conn.recv(1024)
        if not msg:
            break
        decoded_msg = msg.decode("utf-8")
        print(decoded_msg)

    conn.close()


def main():
    run_server()


main()
