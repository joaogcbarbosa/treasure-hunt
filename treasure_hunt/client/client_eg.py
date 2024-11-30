from socket import socket, AF_INET, SOCK_STREAM
from ..constants import SERVER_PORT, SERVER_HOST
from time import sleep

msg = "oi"

client_socket_1 = socket(family=AF_INET, type=SOCK_STREAM)
client_socket_1.connect((SERVER_HOST, SERVER_PORT))
client_socket_1.send(msg.encode("utf-8"))
sleep(3)
client_socket_2 = socket(family=AF_INET, type=SOCK_STREAM)
client_socket_2.connect((SERVER_HOST, SERVER_PORT))
client_socket_2.send(msg.encode("utf-8"))
sleep(3)
client_socket_3 = socket(family=AF_INET, type=SOCK_STREAM)
client_socket_3.connect((SERVER_HOST, SERVER_PORT))
client_socket_3.send(msg.encode("utf-8"))
