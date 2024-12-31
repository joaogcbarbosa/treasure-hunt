from contextlib import contextmanager
from socket import AF_INET, SOCK_STREAM, socket
from typing import Any, Generator


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
