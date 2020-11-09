from board1 import Board1
from game1 import Game1

def main():

    # row_input = int(input("Please enter number of rows: "))
    # col_input = int(input("Please enter number of columns: "))
    # n_input = int(input("Please enter n-in-a-row: "))
    row_input = 3
    col_input = 6
    n_input = 3

    print("\nPlaying game with rows={}, cols={}, and n-in-a-row={}".format(row_input, col_input, n_input))
    print("Calculating minimax for entire game tree!\n\n")

    start_board = Board1(row_input, col_input, n_input)
    transposition_table = {}

    Game1(start_board, transposition_table)

    return 0


if __name__ == "__main__":
    main()
