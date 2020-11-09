from game import Game


def main():

    print("Available Games:")
    print("-------------------------------------------------------------")
    print("1. Connect 3 / 4 with minimax for entire game tree")
    print("2. Connect 3 / 4 with alpha-beta pruning and limited depth")
    game_type = int(input("Please select the game you would like to play by number: "))

    Game(game_type)

    return 0


if __name__ == "__main__":
    main()
