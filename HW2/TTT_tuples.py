from typing import List, Tuple
from itertools import permutations


def print_board(gameboard: List) -> List:
    # print game board
    print("-------------")
    for i in range(3):
        print("|", gameboard[0 + i * 3], "|", gameboard[1 + i * 3], "|", gameboard[2 + i * 3], "|")
    print("-------------")
    return gameboard


def change_player(player: str) -> str:
    player = 'X' if player == '0' else '0'
    return player


def find_winner(moves: Tuple) -> int:
    '''
    :param moves: user's moves
    :return: index of elemenr which we can use for find winner in gameboard
    '''

    winner_combinations = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    )
    # permutations is all combinations with 3 digits which had been inputed by user
    possible_moves = permutations(moves, 3)
    # if it in winner_combinations, mean that somebody won
    for move in possible_moves:
        if move in winner_combinations:
            return move[1]


def play_game():
    game_continue: bool = True

    player: str = 'X'

    gameboard = [i for i in range(1, 10)]

    users_moves: List = []

    x_moves: tuple = ()
    o_moves: tuple = ()

    while game_continue:

        print_board(gameboard)

        position: int = int(input(f'Where you wanna move player {player}?'))

        if position not in range(1, 10):
            print('Incorrect position')
            continue
        elif gameboard[position - 1] == 'X' or gameboard[position - 1] == 'O':
            print('This place is fill.Choose new place')
            continue
        # if two conditions were fulfilled we can take X or O
        else:
            gameboard[position - 1] = player
            users_moves.append(position - 1)
            # x player moves is even elements of list
            x_moves = tuple(set(x_moves + (tuple(item for i, item in enumerate(users_moves) if i % 2 == 0))))
            # O player moves is odd elements of list
            o_moves = tuple(set(o_moves + (tuple(item for i, item in enumerate(users_moves) if i % 2 != 0))))

        player = change_player(player)

        # digit or None == digit

        winner = find_winner(x_moves) or find_winner(o_moves)

        if winner is not None:
            print(f"{gameboard[winner]} win!!!")
            break

        if len(x_moves)+len(o_moves) == 9:
            print("Nobody hasn't won!")
            break

play_game()
