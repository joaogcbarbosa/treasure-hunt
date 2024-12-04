from treasure_hunt.utils.templates import treasure_hunt_title, number_of_players
from treasure_hunt.utils.checks import check_number_of_players
from treasure_hunt.server.server import run_server


if __name__ == "__main__":
    # Terminal Template
    treasure_hunt_title()
    number_of_players()
    # =================
    nro_players = check_number_of_players()
    run_server(nro_players)
    # connecting players...
    # starting game...
