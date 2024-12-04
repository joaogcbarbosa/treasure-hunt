from treasure_hunt.client.client import client
from treasure_hunt.utils.constants import SERVER_PORT, SERVER_HOST
import json

if __name__ == "__main__":
    with client(SERVER_HOST, SERVER_PORT) as c:
        while True:
            data = c.recv(1024)
            if not data:
                print("Server has reached its limit of connections.")
                break
            data = c.recv(1024).decode("utf-8")
            data = json.loads(data)
            print(data["map_situation"])
            choose = input(data["your_turn_sentence"])
