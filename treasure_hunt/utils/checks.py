from .constants import MAX_PLAYERS, MIN_PLAYERS
from .templates import number_of_players_warn


def check_number_of_players() -> int:
    nro_players = int(input().strip())
    while nro_players > MAX_PLAYERS or nro_players < MIN_PLAYERS:
        number_of_players_warn()
        nro_players = int(input().strip())
    return nro_players
