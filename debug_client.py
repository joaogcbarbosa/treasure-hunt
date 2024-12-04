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
            map_situation = data["map_situation"]
            your_turn_sentence = data["your_turn_sentence"]
            print(map_situation)
            possible_moves = check_possible_moves(map_situation)
            choose = input(your_turn_sentence)
