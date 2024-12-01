from treasure_hunt.client.client import client

if __name__ == "__main__":
    with client() as c:
        while True:
            pass  # just checking connection
