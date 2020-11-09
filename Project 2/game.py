import numpy as np
from board import Board
from minimax import Minimax
from timeit import default_timer as timer


class Game:

    def __init__(self, game_type):

        self.turn = True
        self.winner = False
        self.game_type = game_type

        self.row_count, self.col_count, self.win_cond, self.depth_cutoff = self.getUserInput()
        self.current_state = Board(self.row_count, self.col_count, self.win_cond)
        self.table = {}

        if self.game_type == 1:
            print("\nPlaying game with rows={}, cols={}, and n-in-a-row={}".format(self.row_count, self.col_count, self.win_cond))
            print("Calculating minimax for entire game tree!\n\n")

            self.minimax_value = self.calcMinimax()

            self.runGame()
        else:
            print("\nPlaying game with rows={}, cols={}, and n-in-a-row={}".format(self.row_count, self.col_count, self.win_cond))

            self.runGame()

    def getUserInput(self):
        row_input = int(input("\nPlease enter number of rows: "))
        col_input = int(input("Please enter number of columns: "))
        n_input = int(input("Please enter n-in-a-row: "))
        if self.game_type == 2:
            depth_input = int(input("Please enter cutoff depth: "))
            return row_input, col_input, n_input, depth_input
        return row_input, col_input, n_input, None


    def calcMinimax(self):

        minimax_start = timer()
        minimax_value = self.minimax(self.current_state)
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

    def minimax(self, state):

        if state in self.table:
            return self.table[state].minimax_value

        state.updateWinCheck()
        if state.isTerminal():
            u = state.stateUtility()
            self.table[state] = Minimax(u, None)
            return u
        elif state.turn == "MAX":
            best_minimax_so_far = np.NINF
            best_move_for_state = None

            children_states = state.genNextBoards()
            for i in range(len(state.moves)):
                if state.moves[i]:
                    child_state = children_states[i]
                    minimax_of_child = self.minimax(child_state)
                    if minimax_of_child > best_minimax_so_far:
                        best_minimax_so_far = minimax_of_child
                        best_move_for_state = i
            self.table[state] = Minimax(best_minimax_so_far, best_move_for_state)
            return best_minimax_so_far
        else:
            best_minimax_so_far = np.Inf
            best_move_for_state = None

            children_states = state.genNextBoards()
            for i in range(len(state.moves)):
                if state.moves[i]:
                    child_state = children_states[i]
                    minimax_of_child = self.minimax(child_state)
                    if minimax_of_child < best_minimax_so_far:
                        best_minimax_so_far = minimax_of_child
                        best_move_for_state = i
            self.table[state] = Minimax(best_minimax_so_far, best_move_for_state)
            return best_minimax_so_far

    def alphaBeta(self, state, alpha, beta, depth):

        if state in self.table:
            return self.table[state].minimax_value

        state.updateWinCheck()
        if state.isTerminal():
            u = state.stateUtility()
            self.table[state] = Minimax(u, None)
            return u
        elif depth >= self.depth_cutoff:
            e = state.stateEval()
            self.table[state] = Minimax(e, None)
            return e
        elif state.turn == "MAX":
            best_minimax_so_far = np.NINF
            best_move_for_state = None

            children_states = state.genNextBoards()
            for i in range(len(state.moves)):
                if state.moves[i]:
                    child_state = children_states[i]
                    minimax_of_child = self.alphaBeta(child_state, alpha, beta, depth + 1)
                    if minimax_of_child > best_minimax_so_far:
                        best_minimax_so_far = minimax_of_child
                        best_move_for_state = i
                    if best_minimax_so_far >= beta:
                        return best_minimax_so_far
                    alpha = max(alpha, best_minimax_so_far)
            self.table[state] = Minimax(best_minimax_so_far, best_move_for_state)
            return best_minimax_so_far
        else:
            best_minimax_so_far = np.Inf
            best_move_for_state = None

            children_states = state.genNextBoards()
            for i in range(len(state.moves)):
                if state.moves[i]:
                    child_state = children_states[i]
                    minimax_of_child = self.alphaBeta(child_state, alpha, beta, depth + 1)
                    if minimax_of_child < best_minimax_so_far:
                        best_minimax_so_far = minimax_of_child
                        best_move_for_state = i
                    if best_minimax_so_far <= alpha:
                        return best_minimax_so_far
                    beta = min(beta, best_minimax_so_far)
            self.table[state] = Minimax(best_minimax_so_far, best_move_for_state)
            return best_minimax_so_far




    def runGame(self):

        print("\nBeginning Game!\n")

        # minimax game
        if self.game_type == 1:
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
                    choice = int(input("What column do you want to move in? "))

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
        # alpha beta game
        else:
            while not self.winner:
                if self.turn:
                    print("Computer's Turn (MAX):")
                    print(self.current_state, end="")
                    minimax_start = timer()
                    minimax = self.alphaBeta(self.current_state, np.NINF, np.Inf, 0)
                    minimax_end = timer()
                    print("Minimax calculation completed in {} ms".format((minimax_end - minimax_start) * 1000))
                    print("Transposition table has {} states".format(len(self.table)))
                    print("The minimax value for this state is {}".format(minimax))
                    move = self.table[self.current_state].state_move
                    print("The best column to move in is {}".format(move))
                    print("The computer picks {}".format(move))

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
                    minimax_start = timer()
                    minimax = self.alphaBeta(self.current_state, np.NINF, np.Inf, 0)
                    minimax_end = timer()
                    print("Minimax calculation completed in {} ms".format((minimax_end - minimax_start) * 1000))
                    print("Transposition table has {} states".format(len(self.table)))
                    print("The minimax value for this state is {}".format(minimax))
                    # print("The best column to move in is {}".format(self.table[self.current_state].state_move))
                    choice = int(input("What column do you want to move in? "))

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
                self.table = {}
                print()
