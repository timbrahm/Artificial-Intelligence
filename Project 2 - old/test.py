import numpy as np


def checkLeftHoriz(arr_state, current_row, current_col, piece):
    horiz_count = 0
    for i in reversed(range(current_col)):
        if arr_state[current_row][i] == piece:
            horiz_count += 1
        else:
            return horiz_count
    return horiz_count
def checkRightHoriz(arr_state, current_row, current_col, c_count, piece):
    horiz_count = 0
    for i in range(current_col + 1, c_count):
        if arr_state[current_row][i] == piece:
            horiz_count += 1
        else:
            return horiz_count
    return horiz_count
# horiz_count = 0
# for i in reversed(range(curr_col)):
#     if arr[curr_row][i] == last_piece:
#         horiz_count += 1
#     else:
#         break
# for i in range(curr_col + 1, col_count):
#     if arr[curr_row][i] == last_piece:
#         horiz_count += 1
#     else:
#         break
# print("horiz: {}".format(horiz_count))

# Check for vertical win
def checkVert(arr_state, current_row, current_col, r_count, piece):
    vert_count = 0
    for i in range(current_row + 1, r_count):
        if arr_state[i][current_col] == piece:
            vert_count += 1
        else:
            return vert_count
    return vert_count
# vert_count = 0
# for i in range(curr_row + 1, row_count):
#     if arr[i][curr_col] == last_piece:
#         vert_count += 1
#     else:
#         break
# print("vert: {}".format(vert_count))

# Check for positive slope win

def checkLeftPos(arr_state, current_row, current_col, r_count, piece):
    pos_slope_count = 0
    col_var = current_col
    for i in range(current_row + 1, r_count):
        for j in reversed(range(col_var)):
            # print("Left side pos_slope: [{}][{}] = {}".format(i, j, arr_state[i][j]))
            if arr_state[i][j] == piece:
                pos_slope_count += 1
                col_var -= 1
                break
            else:
                return pos_slope_count
    return pos_slope_count
# pos_slope_count = 0
# col_var = curr_col
# for i in range(curr_row + 1, row_count):
#     for j in reversed(range(col_var)):
#         print("Left side pos_slope: [{}][{}] = {}".format(i, j, arr[i][j]))
#         if arr[i][j] == last_piece:
#             pos_slope_count += 1
#             col_var -= 1
#             break
#         else:
#             break
#     break

def checkRightPos(arr_state, current_row, current_col, c_count, piece):
    pos_slope_count = 0
    row_var = current_row
    for j in range(current_col + 1, c_count):
        for i in reversed(range(row_var)):
            # print("Right side pos_slope: [{}][{}] = {}".format(i, j, arr_state[i][j]))
            if arr_state[i][j] == piece:
                pos_slope_count += 1
                row_var -= 1
                break
            else:
                return pos_slope_count
    return pos_slope_count

# row_var = curr_row
# for j in range(curr_col + 1, col_count):
#     for i in reversed(range(row_var)):
#         print("Right side pos_slope: [{}][{}] = {}".format(i, j, arr[i][j]))
#         if arr[i][j] == last_piece:
#             pos_slope_count += 1
#             row_var -= 1
#             break
#         else:
#             break
#     break
# print("pos_slope: {}".format(pos_slope_count))

# Check for negative slope win
def checkLeftNeg(arr_state, current_row, current_col, piece):
    neg_slope_count = 0
    row_var = current_row
    col_var = current_col
    for i in reversed(range(row_var)):
        for j in reversed(range(col_var)):
            if arr_state[i][j] == piece:
                neg_slope_count += 1
                row_var -= 1
                col_var -= 1
                break
            else:
                return neg_slope_count
    return neg_slope_count
# neg_slope_count = 0
# row_var = curr_row
# col_var = curr_col
# for i in reversed(range(row_var)):
#     for j in reversed(range(col_var)):
#         if arr[i][j] == last_piece:
#             neg_slope_count += 1
#             row_var -= 1
#             col_var -= 1
#             break
#         else:
#             break

def checkRightNeg(arr_state, current_row, current_col, r_count, c_count, piece):
    neg_slope_count = 0
    row_var = current_row
    col_var = current_col
    for i in range(row_var + 1, r_count):
        for j in range(col_var + 1, c_count):
            if arr_state[i][j] == piece:
                neg_slope_count += 1
                row_var += 1
                col_var += 1
                break
            else:
                return neg_slope_count
    return neg_slope_count


arr = [[2, 0, 0, 2, 0],
       [1, 1, 0, 1, 2],
       [2, 2, 0, 2, 1],
       [1, 1, 2, 1, 1]]
arr = np.array(arr)

print(np.count_nonzero(arr == 2))
for piece in arr:
    print(piece)


row_count = 4
col_count = 5

last_move = 4

piece_tracker = [4, 4, 1, 4, 3]

curr_row = row_count - piece_tracker[last_move]
curr_col = last_move
last_piece = arr[curr_row][curr_col]


# right_horiz = checkRightHoriz(arr, curr_row, curr_col, col_count, last_piece)
# left_horiz = checkLeftHoriz(arr, curr_row, curr_col, last_piece)
# horiz_check = right_horiz + left_horiz
# print("horiz: {}".format(horiz_check))
#
# vert = checkVert(arr, curr_row, curr_col, row_count, last_piece)
# print("vert: {}".format(vert))
#
# right_pos = checkRightPos(arr, curr_row, curr_col, col_count, last_piece)
# left_pos = checkLeftPos(arr, curr_row, curr_col, row_count, last_piece)
# pos_slope_check = right_pos + left_pos
# print("pos_slope_check: {}".format(pos_slope_check))
#
# right_neg = checkRightNeg(arr, curr_row, curr_col, row_count, col_count, last_piece)
# left_neg = checkLeftNeg(arr, curr_row, curr_col, last_piece)
# neg_slope_check = right_neg + left_neg
# print("neg_slope_check: {}".format(neg_slope_check))


# row_var = curr_row
# col_var = curr_col
# for i in range(row_var + 1, row_count):
#     for j in range(col_var + 1, col_count):
#         if arr[i][j] == last_piece:
#             neg_slope_count += 1
#             row_var += 1
#             col_var += 1
#             break
#         else:
#             break
# print("neg_slope: {}".format(neg_slope_count))



# # Check for horizontal win
# horiz_count = 0
# for i in reversed(range(curr_col)):
#     if arr[curr_row][i] == last_piece:
#         horiz_count += 1
#     else:
#         break
# for i in range(curr_col + 1, col_count):
#     if arr[curr_row][i] == last_piece:
#         horiz_count += 1
#     else:
#         break
# print("horiz: {}".format(horiz_count))
#
#
#
# # Check for vertical win
# vert_count = 0
# for i in range(curr_row + 1, row_count):
#     if arr[i][curr_col] == last_piece:
#         vert_count += 1
#     else:
#         break
# print("vert: {}".format(vert_count))
#
# neg_slope_count = 0
# row_var = curr_row
# col_var = curr_col
# for i in reversed(range(row_var)):
#     for j in reversed(range(col_var)):
#         print("Left side neg_slope: [{}][{}] = {}".format(i, j, arr[i][j]))
#         if arr[i][j] == last_piece:
#             neg_slope_count += 1
#             row_var -= 1
#             col_var -= 1
#             break
#         else:
#             break
# row_var = curr_row
# col_var = curr_col
# for i in range(row_var + 1, row_count):
#     for j in range(col_var + 1, col_count):
#         print("Right side neg_slope: [{}][{}] = {}".format(i, j, arr[i][j]))
#         if arr[i][j] == last_piece:
#             neg_slope_count += 1
#             row_var += 1
#             col_var += 1
#             break
#         else:
#             break
# print("neg_slope: {}".format(neg_slope_count))
#
# pos_slope_count = 0
# col_var = curr_col
# for i in range(curr_row + 1, row_count):
#     for j in reversed(range(col_var)):
#         print("Left side pos_slope: [{}][{}] = {}".format(i, j, arr[i][j]))
#         if arr[i][j] == last_piece:
#             pos_slope_count += 1
#             col_var -= 1
#             break
#         else:
#             col_var -= 1
#             break
#
# row_var = curr_row
# for j in range(curr_col + 1, col_count):
#     for i in reversed(range(row_var)):
#         print("Right side pos_slope: [{}][{}] = {}".format(i, j, arr[i][j]))
#         if arr[i][j] == last_piece:
#             pos_slope_count += 1
#             row_var -= 1
#             break
#         else:
#             break
#     break
#
# print("pos_slope: {}".format(pos_slope_count))




