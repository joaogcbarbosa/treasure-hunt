from treasure_hunt.client.client import client, send_message
from time import sleep

def options_template():
    print("#"*20)
    print("Press [S] to send message.")
    print("Press [Q] to quit.")
    print("#"*20)


if __name__ == "__main__":
    with client() as c:
        while True:
            options_template()
            choice = input("Choose an option: ")
            if choice == "S":
                msg = input("Message: ")
                send_message(msg, c)
            else:
                break
