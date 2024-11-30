from treasure_hunt.client.client import client, send_message
from treasure_hunt.utils import options

if __name__ == "__main__":
    with client() as c:
        while True:
            options()
            choice = input("Choose an option: ")
            if choice == "S":
                msg = input("Message: ")
                send_message(msg, c)
            else:
                break
