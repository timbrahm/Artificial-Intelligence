import numpy as np
from timeit import default_timer as timer


class Board1:

    def __init__(self, row_input, col_input, n_input, turn="MAX", state=None, depth=0, piece_tracker=None, last_move=None):

        self.row_count = row_input
        self.col_count = col_input
        self.win_cond = n_input
        self.board_state = state
        self.turn = turn
        self.depth = depth
        self.last_move = last_move

        if piece_tracker is not None:
            self.piece_tracker = piece_tracker
        else:
            self.piece_tracker = np.zeros(self.col_count, dtype=int)

        self.board_state = self.createBoard()

        self.moves = self.availableMoves()

        self.board_create_timer = 0
        self.board_check_timer = 0

    def __str__(self):

        self.printBoard()
        return ""


    def __hash__(self):

        return hash((self.board_state.tostring(), self.turn))


    def __eq__(self, other):

        if isinstance(other, type(self)):
            check_list = [
                other.win_cond == self.win_cond,
                other.turn == self.turn,
                self.isEqual(other)
            ]
            if all(check_list):
                return True

        return False


    def isEqual(self, other):

        return np.array_equal(self.board_state, other.board_state)


    def printBoard(self):

        for i in range(self.board_state.shape[0]):
            for j in range(self.board_state.shape[1]):
                if self.board_state[i][j] == 0:
                    print('.', end='')
                elif self.board_state[i][j] == 1:
                    print('x', end='')
                else:
                    print('o', end='')
            print()


    def createBoard(self):

        if self.board_state is not None:
            return self.board_state
        else:
            return np.zeros((self.row_count, self.col_count))


    def availableMoves(self):
        # if self.win_check:
        #     return None

        return [True if i == 0 else False for i in self.board_state[0]]


    def isTerminal(self):

        board_check_start = timer()
        check = self.isWin()[0] or not any(self.moves)
        board_check_end = timer()

        self.board_check_timer += (board_check_end - board_check_start)

        return check

    def alternateIsTerminal(self):
        win_check = self.alternateIsWin()

        if win_check is None:
            return not any(self.moves)

        board_check_start = timer()
        check = win_check[0] or not any(self.moves)
        board_check_end = timer()

        self.board_check_timer += (board_check_end - board_check_start)

        return check

    def stateUtility(self):

        state_value = 0
        winner = self.isWin()
        if winner[1] == "MAX":
            state_value = int(10000 * self.row_count * self.col_count / self.depth)
        elif winner[1] == "MIN":
            state_value = -1 * int(10000 * self.row_count * self.col_count / self.depth)
        elif self.isTerminal() and winner[0] == False:
            state_value = 0
        return state_value


    def genNextBoards(self):

        board_create_start = timer()

        board_list = {}

        for i in range(len(self.moves)):
            if self.moves[i]:
                new_board = self.board_state.copy()
                new_piece_tracker = self.piece_tracker.copy()
                if self.turn == "MAX":
                    new_board[self.row_count - new_piece_tracker[i] - 1][i] = 1
                    new_piece_tracker[i] += 1
                    new_board = Board1(self.row_count, self.col_count, self.win_cond, "MIN", state=new_board,
                                                              depth=self.depth + 1, piece_tracker=new_piece_tracker, last_move=i)
                else:
                    new_board[self.row_count - new_piece_tracker[i] - 1][i] = 2
                    new_piece_tracker[i] += 1
                    new_board = Board1(self.row_count, self.col_count, self.win_cond, "MAX", state=new_board,
                                                              depth=self.depth + 1, piece_tracker=new_piece_tracker, last_move=i)

                board_list[i] = new_board

        board_create_end = timer()
        self.board_create_timer += (board_create_end - board_create_start)


        return board_list

    # def genNextBoards(self):
    #
    #     # if self.moves is None:
    #     #     return None
    #
    #     board_create_start = timer()
    #
    #     board_list = []
    #
    #     board_transpose = self.board_state.T
    #
    #     for i in range(len(self.moves)):
    #         if self.moves[i]:
    #             new_board = self.board_state.copy()
    #             for j in range(1, len(board_transpose[i]) + 1):
    #                 row = j - 1
    #                 if j == len(board_transpose[i]):
    #                     if self.turn == "MAX":
    #                         new_board[self.row_count - 1][i] = 1
    #
    #                         new_board = Board(self.row_count, self.col_count, self.win_cond, "MIN", new_board,
    #                                           self.depth + 1)
    #                     else:
    #                         new_board[self.row_count - 1][i] = 2
    #
    #                         new_board = Board(self.row_count, self.col_count, self.win_cond, "MAX", new_board,
    #                                           self.depth + 1)
    #
    #                     board_list += [new_board]
    #                     break
    #                 else:
    #                     if board_transpose[i][j] != 0:
    #                         if self.turn == "MAX":
    #                             new_board[row][i] = 1
    #
    #                             new_board = Board(self.row_count, self.col_count, self.win_cond, "MIN", new_board, self.depth + 1)
    #
    #                         else:
    #                             new_board[row][i] = 2
    #
    #                             new_board = Board(self.row_count, self.col_count, self.win_cond, "MAX", new_board, self.depth + 1)
    #
    #                         board_list += [new_board]
    #
    #                         break
    #
    #     board_create_end = timer()
    #     self.board_create_timer += (board_create_end - board_create_start)
    #
    #
    #     return board_list


    def isWin(self):

        if self.depth < (2 * self.win_cond) - 1:
            return False, None

        # Check horizontals
        if self.win_cond == 4:
            for col in range(self.col_count - 3):
                for row in range(self.row_count):
                    if self.board_state[row][col] == 1 and self.board_state[row][col + 1] == 1 and self.board_state[row][col + 2] == 1 and self.board_state[row][col + 3] == 1:
                        return True, "MAX"
                    elif self.board_state[row][col] == 2 and self.board_state[row][col + 1] == 2 and self.board_state[row][col + 2] == 2 and self.board_state[row][col + 3] == 2:
                        return True, "MIN"
        else:
            for col in range(self.col_count - 2):
                for row in range(self.row_count):
                    if self.board_state[row][col] == 1 and self.board_state[row][col + 1] == 1 and self.board_state[row][col + 2] == 1:
                        return True, "MAX"
                    elif self.board_state[row][col] == 2 and self.board_state[row][col + 1] == 2 and self.board_state[row][col + 2] == 2:
                        return True, "MIN"

        # Check verticals
        if self.win_cond == 4:
            for col in range(self.col_count):
                for row in range(self.row_count - 3):
                    if self.board_state[row][col] == 1 and self.board_state[row + 1][col] == 1 and self.board_state[row + 2][col] == 1 and self.board_state[row + 3][col] == 1:
                        return True, "MAX"
                    elif self.board_state[row][col] == 2 and self.board_state[row + 1][col] == 2 and self.board_state[row + 2][col] == 2 and self.board_state[row + 3][col] == 2:
                        return True, "MIN"
        else:
            for col in range(self.col_count):
                for row in range(self.row_count - 2):
                    if self.board_state[row][col] == 1 and self.board_state[row + 1][col] == 1 and self.board_state[row + 2][col] == 1:
                        return True, "MAX"
                    elif self.board_state[row][col] == 2 and self.board_state[row + 1][col] == 2 and self.board_state[row + 2][col] == 2:
                        return True, "MIN"

        # Check positive slope
        if self.win_cond == 4:
            for col in range(self.col_count - 3):
                for row in range(self.row_count - 3):
                    if self.board_state[row][col] == 1 and self.board_state[row + 1][col + 1] == 1 and self.board_state[row + 2][col + 2] == 1 and self.board_state[row + 3][col + 3] == 1:
                        return True, "MAX"
                    elif self.board_state[row][col] == 2 and self.board_state[row + 1][col + 1] == 2 and self.board_state[row + 2][col + 2] == 2 and self.board_state[row + 3][col + 3] == 2:
                        return True, "MIN"
        else:
            for col in range(self.col_count - 2):
                for row in range(self.row_count - 2):
                    if self.board_state[row][col] == 1 and self.board_state[row + 1][col + 1] == 1 and self.board_state[row + 2][col + 2] == 1:
                        return True, "MAX"
                    elif self.board_state[row][col] == 2 and self.board_state[row + 1][col + 1] == 2 and self.board_state[row + 2][col + 2] == 2:
                        return True, "MIN"

        # Check negative slope
        if self.win_cond == 4:
            for col in range(self.col_count - 3):
                for row in range(3, self.row_count):
                    if self.board_state[row][col] == 1 and self.board_state[row - 1][col + 1] == 1 and self.board_state[row - 2][col + 2] == 1 and self.board_state[row - 3][col + 3] == 1:
                        return True, "MAX"
                    elif self.board_state[row][col] == 2 and self.board_state[row - 1][col + 1] == 2 and self.board_state[row - 2][col + 2] == 2 and self.board_state[row - 3][col + 3] == 2:
                        return True, "MIN"
        else:
            for col in range(self.col_count - 2):
                for row in range(2, self.row_count):
                    if self.board_state[row][col] == 1 and self.board_state[row - 1][col + 1] == 1 and self.board_state[row - 2][col + 2] == 1:
                        return True, "MAX"
                    elif self.board_state[row][col] == 2 and self.board_state[row - 1][col + 1] == 2 and self.board_state[row - 2][col + 2] == 2:
                        return True, "MIN"

        return False, None

    def checkLeftHoriz(self, curr_row, curr_col, piece):
        horiz_count = 0
        for i in reversed((range(curr_col))):
            if self.board_state[curr_row][i] == piece:
                horiz_count += 1
            else:
                return horiz_count
        return horiz_count

    def checkRightHoriz(self, curr_row, curr_col, piece):
        horiz_count = 0
        for i in range(curr_col + 1, self.col_count):
            if self.board_state[curr_row][i] == piece:
                horiz_count += 1
            else:
                return horiz_count
        return horiz_count

    def checkVert(self, curr_row, curr_col, piece):
        vert_count = 0
        for i in range(curr_row + 1, self.row_count):
            if self.board_state[i][curr_col] == piece:
                vert_count += 1
            else:
                return vert_count
        return vert_count

    def checkLeftPosSlope(self, curr_row, curr_col, piece):
        pos_slope_count = 0
        col_var = curr_col
        for i in range(curr_row + 1, self.row_count):
            for j in reversed(range(col_var)):
                if self.board_state[i][j] == piece:
                    pos_slope_count += 1
                    col_var -= 1
                    break
                else:
                    return pos_slope_count
        return pos_slope_count

    def checkRightPosSlope(self, curr_row, curr_col, piece):
        pos_slope_count = 0
        row_var = curr_row
        for j in range(curr_col + 1, self.col_count):
            for i in reversed(range(row_var)):
                if self.board_state[i][j] == piece:
                    pos_slope_count += 1
                    row_var -= 1
                    break
                else:
                    return pos_slope_count
        return pos_slope_count

    def checkLeftNegSlope(self, curr_row, curr_col, piece):
        neg_slope_count = 0
        row_var = curr_row
        col_var = curr_col
        for i in reversed(range(row_var)):
            for j in reversed(range(col_var)):
                if self.board_state[i][j] == piece:
                    neg_slope_count += 1
                    row_var -= 1
                    col_var -= 1
                    break
                else:
                    return neg_slope_count
        return neg_slope_count

    def checkRightNegSlope(self, curr_row, curr_col, piece):
        neg_slope_count = 0
        row_var = curr_row
        col_var = curr_col
        for i in range(row_var + 1, self.row_count):
            for j in range(col_var + 1, self.col_count):
                if self.board_state[i][j] == piece:
                    neg_slope_count += 1
                    row_var += 1
                    col_var += 1
                    break
                else:
                    return neg_slope_count
        return neg_slope_count

    def alternateIsWin(self):

        if self.depth < (2 * self.win_cond) - 1:
            return False, None

        curr_row = self.row_count - self.piece_tracker[self.last_move]
        curr_col = self.last_move
        last_piece = self.board_state[curr_row][curr_col]

        # Check for horizontal win
        right_horiz_check = self.checkRightHoriz(curr_row, curr_col, last_piece)
        left_horiz_check = self.checkLeftHoriz(curr_row, curr_col, last_piece)
        horiz_count = right_horiz_check + left_horiz_check
        if horiz_count >= self.win_cond - 1:
            if last_piece == 1:
                return True, "MAX"
            else:
                return True, "MIN"

        # Check for vertical win
        vert_count = self.checkVert(curr_row, curr_col, last_piece)
        if vert_count >= self.win_cond - 1:
            if last_piece == 1:
                return True, "MAX"
            else:
                return True, "MIN"

        # Check for positive slope win
        right_pos_check = self.checkRightPosSlope(curr_row, curr_col, last_piece)
        left_pos_check = self.checkLeftPosSlope(curr_row, curr_col, last_piece)
        pos_slope_count = right_pos_check + left_pos_check
        if pos_slope_count >= self.win_cond - 1:
            if last_piece == 1:
                return True, "MAX"
            else:
                return True, "MIN"

        # Check for negative slope win
        right_neg_check = self.checkRightNegSlope(curr_row, curr_col, last_piece)
        left_neg_check = self.checkLeftNegSlope(curr_row, curr_col, last_piece)
        neg_slope_count = right_neg_check + left_neg_check
        if neg_slope_count >= self.win_cond - 1:
            if last_piece == 1:
                return True, "MAX"
            else:
                return True, "MIN"

        return False, None
