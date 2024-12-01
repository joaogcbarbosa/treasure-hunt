from treasure_hunt.utils.templates import treasure_hunt_title, number_of_players
from multiprocessing.pool import ThreadPool
from treasure_hunt.utils.checks import check_number_of_players


if __name__ == "__main__":
    treasure_hunt_title()
    number_of_players()
    nro_players = check_number_of_players()
    # starting server..
    # connecting players...
    # starting game...
