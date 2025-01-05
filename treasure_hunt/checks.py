from itertools import product
from time import sleep
from typing import Union

from .constants import MAX_PLAYERS, MIN_PLAYERS
from .templates import number_of_players, number_of_players_warn


def check_number_of_players() -> int:
    """
    Função para input da quantidade de jogadores para a partida.

    Não deixa nenhum outro número inteiro que não esteja dentro do limite
    mínimo e máximo de jogadores ser inputado.
    """
    nro_players = int(input().strip())
    while nro_players > MAX_PLAYERS or nro_players < MIN_PLAYERS:
        number_of_players_warn()
        sleep(1.5)
        number_of_players()
        nro_players = int(input().strip())
    return nro_players


def check_available_moves(
    surrounding_positions: list[tuple[int]], game_map: list[list[Union[int, str]]]
) -> list[tuple[int]]:
    """
    Função responsável por analisar as "redondezas" da posição do jogador (cima, baixo, direita, esquerda).
    Se em volta do jogador tiverem strings como "X", "P2" ou alguma posição fora dos limites do mapa,
    os possíveis movimentos do jogador diminuirão.
    """

    # Todas posições do mapa
    map_positions = [(i, j) for i in range(len(game_map)) for j in range(len(game_map))]

    surrounding_positions_copy = (
        surrounding_positions.copy()
    )  # Posições em torno da posição que o jogador está
    for s in surrounding_positions_copy:
        # Se a posição não estiver nos limites do mapa ou se for qualquer string diferente de "X" (pois é o mapa especial),
        # essa posição é removida do leque de possíveis jogadas.
        if s not in map_positions or (
            isinstance(game_map[s[0]][s[1]], str) and game_map[s[0]][s[1]] != "X"
        ):
            surrounding_positions.remove(s)

    return surrounding_positions


def check_player_position(game_map: list[list[Union[int, str]]], player: str) -> tuple[int, int]:
    """
    Função responsável por achar a atual posição do jogador.
    """
    x: int
    y: int
    for i, j in product(range(len(game_map)), range(len(game_map))):
        if isinstance(game_map[i][j], str) and game_map[i][j] == player:
            x = i
            y = j
            break

    return x, y


def check_possible_moves(
    player: str, game_map: list[list[Union[int, str]]]
) -> tuple[list[tuple[int]], tuple[int, int]]:

    player_pos = check_player_position(game_map, player)
    x, y = player_pos

    surrounding_positions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    available_moves = check_available_moves(surrounding_positions, game_map)

    return available_moves, player_pos
