from treasure_hunt.client.client_eg import client, send_message
from time import sleep

if __name__ == "__main__":
    with client() as c:
        send_message("Oi", c)
        sleep(5)
        send_message("Oi de novo", c)
