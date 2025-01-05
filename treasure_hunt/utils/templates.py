from treasure_hunt.models.map import GameMap, SpecialGameMap

# Mensagens no terminal
# =======================================================
def header():
    print("\n" + "=" * 40)


def footer():
    print("=" * 40)


def treasure_hunt_title():
    header()
    print("        🌟 TREASURE-HUNT 🌟")
    footer()


def number_of_players():
    header()
    print("Select number of players: ")
    print("Press [2] for two players")
    print("Press [3] for three players")
    footer()


def number_of_players_warn():
    print("Please select a possible number of players.")
# =======================================================


def show_map(game_map: GameMap | SpecialGameMap) -> None:
    """
    Envolve o print do mapa de uma forma se for o mapa principal
    e com estrelas se for o mapa especial.
    """
    if isinstance(game_map, GameMap):
        print("===============")
        print(game_map.display())
        print("===============")
        return
    print("=*=*=*=*=*=*=*=")
    print(game_map.display())
    print("=*=*=*=*=*=*=*=")
