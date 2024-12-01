from socket import socket, AF_INET, SOCK_STREAM
from typing import Any, Generator
from time import sleep
from contextlib import contextmanager

@contextmanager
def client(host: str, port: int) -> Generator[socket, Any, Any]:
    try:
        client_socket = socket(family=AF_INET, type=SOCK_STREAM)
        client_socket.connect((host, port))
        yield client_socket
    except Exception as e:
        print(f"Could not connect: {e}")
    finally:
        client_socket.close()


def send_message(msg: str, client: socket) -> None:
    client.send(msg.encode("utf-8"))
