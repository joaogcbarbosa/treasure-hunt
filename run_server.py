from treasure_hunt.utils.templates import treasure_hunt_title, number_of_players
from treasure_hunt.utils.checks import check_number_of_players
from treasure_hunt.server.server import server_runner

def main():
    # Terminal Template
    treasure_hunt_title()  # TODO: deve aparecer para o player
    number_of_players()
    # =================
    nro_players = check_number_of_players()
    server_runner(nro_players)


if __name__ == "__main__":
    main()
