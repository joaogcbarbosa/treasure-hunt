from treasure_hunt.client.client import client

if __name__ == "__main__":
    with client() as c:
        while True:
            data = c.recv(1024)
            if not data:  # Se data for vazio, a conexão foi fechada
                print("Server has reached its limit of connections.")
                break
