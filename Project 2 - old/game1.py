from minimax1 import Minimax1
import numpy as np
from timeit import default_timer as timer


def minimax(state, table):
    if state in table.keys():
        return table[state].minimax_value
    elif state.isTerminal():
        u = state.stateUtility()
        table[state] = Minimax1(u, None)
        return u
    elif state.turn == "MAX":
        best_minimax_so_far = np.NINF
        best_move_for_state = None

        children_states = state.genNextBoards()
        for i in range(len(state.moves)):
            if state.moves[i]:
                child_state = children_states[i]
                minimax_of_child = minimax(child_state, table)
                if minimax_of_child > best_minimax_so_far:
                    best_minimax_so_far = minimax_of_child
                    best_move_for_state = i
        table[state] = Minimax1(best_minimax_so_far, best_move_for_state)
        return best_minimax_so_far
    else:
        best_minimax_so_far = np.Inf
        best_move_for_state = None

        children_states = state.genNextBoards()
        for i in range(len(state.moves)):
            if state.moves[i]:
                child_state = children_states[i]
                minimax_of_child = minimax(child_state, table)
                if minimax_of_child < best_minimax_so_far:
                    best_minimax_so_far = minimax_of_child
                    best_move_for_state = i
        table[state] = Minimax1(best_minimax_so_far, best_move_for_state)
        return best_minimax_so_far


class Game1:

    def __init__(self, start_board, table):

        self.turn = True
        self.winner = False
        self.current_state = start_board
        self.table = table

        self.minimax_value = self.calcMinimax()

        # self.runGame()


    def calcMinimax(self):

        minimax_start = timer()
        minimax_value = minimax(self.current_state, self.table)
        minimax_end = timer()
        print("Minimax calculation completed in {} s".format(minimax_end - minimax_start))
        print("Transposition table has {} states".format(len(self.table)))
        print("Minimax value of start state is {}".format(minimax_value))
        if minimax_value > 0:
            print("First player (MAX) has a guaranteed win!")
        elif minimax_value < 0:
            print("Second player (MIN) has a guaranteed win!")
        else:
            print("Neither player has a guaranteed win; game will end in tie with perfect play on both sides.")
        return minimax_value

    def runGame(self):

        print("\nBeginning Game!\n")

        while not self.winner:

            if self.turn:
                print("Computer's Turn (MAX):")
                print(self.current_state, end="")
                print(
                    "The minimax value for this state is: {}".format(self.table[self.current_state].minimax_value))
                move = self.table[self.current_state].state_move
                print("The best column to move in is: {}".format(move))
                print("The computer picks: {}".format(move))

                new_state = self.current_state.genNextBoards()[move]
                if new_state.isWin()[0]:
                    print("\nWinner is MAX:")
                    print(new_state)
                    self.winner = True
                elif new_state.isTerminal():
                    print("\nTie!")
                    print(new_state)
                    self.winner = True
            else:
                print("User's Turn (MIN):")
                print(self.current_state, end="")
                print(
                    "The minimax value for this state is: {}".format(self.table[self.current_state].minimax_value))
                print("The best column to move in is: {}".format(self.table[self.current_state].state_move))
                choice = int(input("What column do you want? "))

                new_state = self.current_state.genNextBoards()[choice]
                if new_state.isWin()[0]:
                    print("\nWinner is MIN:")
                    print(new_state)
                    self.winner = True
                elif new_state.isTerminal():
                    print("\nTie!")
                    print(new_state)
                    self.winner = True

            self.current_state = new_state
            self.turn = not self.turn
            print()
