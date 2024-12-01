from treasure_hunt.utils.templates import treasure_hunt_title, number_of_players
from multiprocessing.pool import ThreadPool


if __name__ == "__main__":
    treasure_hunt_title()
    number_of_players()
    nro_players = int(input().strip())
    with ThreadPool(nro_players) as p:
        pass
