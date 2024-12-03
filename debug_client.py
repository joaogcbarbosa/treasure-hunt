from treasure_hunt.client.client import client
from treasure_hunt.utils.constants import SERVER_PORT, SERVER_HOST

if __name__ == "__main__":
    with client(SERVER_HOST, SERVER_PORT) as c:
        while True:
            data = c.recv(1024)
            if not data:  # Se data for vazio, a conexão foi fechada
                print("Server has reached its limit of connections.")
                break
            mensagem = c.recv(1024).decode('utf-8')
            print(mensagem)