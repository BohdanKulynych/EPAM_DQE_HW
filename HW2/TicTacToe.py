from sys import exit

# create gameboard
gameboard = [i for i in range(1, 10)]


def print_board():
    # print game board
    print("-------------")
    for i in range(3):
        print("|", gameboard[0 + i * 3], "|", gameboard[1 + i * 3], "|", gameboard[2 + i * 3], "|")
    print("-------------")


def change_player(player):
    if player == 'X':
        player = 'O'
    else:
        player = 'X'
    return player


def winner():
    # define range of position and after every iteration check if X or I are in winning positions
    empty_positions = range(1, 10)
    for i in range(3):
        # horizontal
        if gameboard[0 + i * 3] == gameboard[1 + i * 3] == gameboard[2 + i * 3] != empty_positions:
            print(str(gameboard[0 + i * 3]) + ' win')
            exit(0)
        # vertical
        if gameboard[i] == gameboard[i + 3] == gameboard[i + 6] != empty_positions:
            print(str(gameboard[i]) + ' win')
            exit(0)
        # diagonal
        if gameboard[0] == gameboard[4] == gameboard[8] != empty_positions or gameboard[2] == gameboard[4] == \
                gameboard[6] != empty_positions:
            print(str(gameboard[4]) + ' win')
            exit(0)


def game():
    player = 'X'
    count = 0

    for i in range(10):
        print_board()
        #input position
        position = int(input("It's your player," + player + ".Move to which place?"))
        # check if our input  position isn't occupied and in range (1-9)
        if position not in range(1, 10):
            print('Incorrect position')
            continue
        elif gameboard[position - 1] == 'X' or gameboard[position - 1] == 'O':
            print('This place is fill.Choose new place')
            continue
        # if two conditions were fulfilled we can take X or O
        else:
            gameboard[position - 1] = player
            count += 1

        player = change_player(player)
        winner()

        if count == 9:
            return 'Game is over'


a = game()
print(a)
