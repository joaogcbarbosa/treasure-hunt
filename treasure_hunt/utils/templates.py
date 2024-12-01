def header():
    print("\n" + "=" * 40)


def footer():
    print("=" * 40)


def treasure_hunt_title():
    header()
    print("        🌟 TREASURE-HUNT 🌟")
    footer()
    print("🪙 Prepare-se para a aventura! 🏴‍☠️\n")


def move_options():
    header()
    print("Press [W] to GO UP.")
    print("Press [S] to GO DOWN.")
    print("Press [A] to GO LEFT.")
    print("Press [D] to GO RIGHT.")
    footer()


def number_of_players():
    header()
    print("Select number of players: ")
    print("Press [2] for two players")
    print("Press [3] for three players")
    footer()


def number_of_players_warn():
    print("Please select a possible number of players.")
