"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Nov. 1, 2023
"""

def is_empty(board):
    for r_list in board:
        for c in r_list:
            if c != " ":
                return False
    return True

def emptyspaces(board):
    L=[]
    for r_list in range(len(board)):
        for c in range(len(board[0])):
            if board[r_list][c] == " ":
                L.append((r_list,c))
    return L



def is_bounded(board, y_end, x_end, length, d_y, d_x):
    end = (y_end + d_y, x_end + d_x)
    start = (y_end - d_y * length, x_end - d_x * length)
    end_bounded = False
    start_bounded = False
    if end[0] < 0 or end[1] < 0 or end[0] > len(board[0]) - 1 or end[1] > len(board[0]) - 1:
        end_bounded = True
    elif board[end[0]][end[1]] != " ":
        end_bounded = True

    if start[0] < 0 or start[1] < 0 or start[0] > len(board[0]) - 1 or start[1] > len(board[0]) - 1:
        start_bounded = True
    elif board[start[0]][start[1]] != " ":
        start_bounded = True

    if end_bounded and start_bounded:
        return "CLOSED"
    elif end_bounded != start_bounded:
        return "SEMIOPEN"
    return "OPEN"



# def detect_row(board, col, y_start, x_start, length, d_y, d_x):
#
#     semi_open_seq_count = 0
#     open_seq_count = 0
#
#     cur_y = y_start
#     cur_x = x_start
#
#     while cur_y >= 0 and cur_y < len(board) and cur_x >= 0 and cur_x < len(board[0]):
#         if board[cur_y][cur_x] == col:
#             cur_length = 1
#             for i in range(length - 1):
#                 cur_y += d_y
#                 cur_x += d_x
#                 if cur_y == 0 or cur_y == len(board) or cur_x == 0 or cur_x == len(board[0]):
#                     if board[cur_y][cur_x] == col:
#                         cur_length += 1
#                     break
#                 elif board[cur_y][cur_x] != col:
#                     break
#                 cur_length += 1
#
#             if cur_length == length:
#                 bound = is_bounded(board, cur_y, cur_x, length, d_y, d_x)
#                 if bound == "SEMIOPEN":
#                     semi_open_seq_count += 1
#                 elif bound == "OPEN":
#                     open_seq_count += 1
#
#         else:
#             cur_y += d_y
#             cur_x += d_x
#
#     return open_seq_count, semi_open_seq_count

# def detect_row(board, col, y_start, x_start, length, d_y, d_x):
#
#     semi_open_seq_count = 0
#     open_seq_count = 0
#
#     cur_y = y_start
#     cur_x = x_start
#
#     while cur_y >= 0 and cur_y < len(board) and cur_x >= 0 and cur_x < len(board[0]):
#         if board[cur_y][cur_x] == col:
#             cur_length = 1
#             for i in range(length - 1):
#                 if cur_y+d_y < 0 or cur_y+d_y > len(board) - 1 or cur_x+d_x < 0 or cur_x+d_x > len(board[0]) - 1:
#                     break
#                 elif board[cur_y+d_y][cur_x+d_x] != col:
#                     cur_y += d_y
#                     cur_x += d_x
#                     break
#                 cur_y += d_y
#                 cur_x += d_x
#                 cur_length += 1
#
#             if cur_length == length:
#                 bound = is_bounded(board, cur_y, cur_x, length, d_y, d_x)
#                 if bound == "SEMIOPEN":
#                     semi_open_seq_count += 1
#                 elif bound == "OPEN":
#                     open_seq_count += 1
#
#         cur_y += d_y
#         cur_x += d_x
#
#     return open_seq_count, semi_open_seq_count

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    semi_open_seq_count = 0
    open_seq_count = 0
    cur_y = y_start
    cur_x = x_start

    while cur_y >= 0 and cur_y < len(board) and cur_x >= 0 and cur_x < len(board[0]):
        cur_length = 0
        while cur_y >= 0 and cur_y < len(board) and cur_x >= 0 and cur_x < len(board[0]) and board[cur_y][cur_x] == col:
            cur_length += 1
            cur_y += d_y
            cur_x += d_x

        if cur_length == length:
            bound = is_bounded(board, cur_y-d_y, cur_x-d_x, length, d_y, d_x)
            if bound == "SEMIOPEN":
                semi_open_seq_count += 1
            elif bound == "OPEN":
                open_seq_count += 1

        cur_y += d_y
        cur_x += d_x

    return open_seq_count, semi_open_seq_count



def detect_rows(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0

    size_y = len(board)
    size_x = len(board[0])

    for y in range(size_y):
        for (dy, dx) in [(0,1), (1,0), (1,1), (1,-1)]:
                osc, sosc = detect_row(board, col, y, 0, length, dy, dx)
                open_seq_count += osc
                semi_open_seq_count += sosc

    for x in range(1, size_x):
        for (dy, dx) in [(0,1), (1,0), (1,1), (1,-1)]:
                osc, sosc = detect_row(board, col, 0, x, length, dy, dx)
                open_seq_count += osc
                semi_open_seq_count += sosc

    return open_seq_count, semi_open_seq_count



def search_max(board):
    Li = emptyspaces(board)
    move_y, move_x = Li[0][0],Li[0][1]
    board[move_y][move_x] = "b"
    maxscore = score(board)
    board[move_y][move_x] = " "
    for e in Li:
        board[e[0]][e[1]] = "b"
        if score(board)>maxscore:
            maxscore = score(board)
            move_y, move_x = e[0], e[1]
        board[e[0]][e[1]] = " "
    return move_y, move_x



def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])



def is_win(board):
    if colourwin("w",board):
        return "White won"
    elif colourwin("b",board):
        return "Black won"
    elif len(emptyspaces(board))==0:
        return "Draw"
    return "Continue Playing"

def colourwin(col, board):
    for i in range(len(board)-5):
        for j in range(len(board[0])-5):
            if board[i][j]==col and board[i][j+1]==col and board[i][j+2]==col and board[i][j+3]==col and board[i][j+4]==col:
                return True
            if board[i][j]==col and board[i+1][j]==col and board[i+2][j]==col and board[i+3][j]==col and board[i+4][j]==col:
                return True
            if board[i][j]==col and board[i+1][j+1]==col and board[i+2][j+2]==col and board[i+3][j+3]==col and board[i+4][j+4]==col:
                return True
            if board[i][j+4]==col and board[i+1][j+3]==col and board[i+2][j+2]==col and board[i+3][j+1]==col and board[i+4][j]==col:
                return True
    return False


def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i)
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))






def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x



def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    # x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    y = 1; x = 0; d_y = 1; d_x = 1; length = 7

    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 7
    x_end = 6

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'CLOSED':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 4; d_x = 1; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0, 1, length, d_y, d_x) == (1, 0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")
        print(detect_row(board, "w", 0, 1, length, d_y, d_x))

def test_detect_rows():
    board = make_empty_board(8)
    case_detect_rows(board, 1, 5, 1, 0, 3, "w", ())
    case_detect_rows(board, 0, 0, 1, 1, 3, "w", ())
    case_detect_rows(board, 6, 1, 0, 1, 4, "w", ())
    case_detect_rows(board, 3, 1, 0, 1, 4, "b", ())

def case_detect_rows(board, y, x, d_y, d_x, length, col, expected):
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    output = detect_rows(board, "w", 3)
    if output == expected:
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")
        print("Expected:", expected, "Got:", output, "\n")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0




if __name__ == '__main__':
    print(play_gomoku(8))
    # test_is_empty()
    # test_is_bounded()
    # test_detect_row()
    #test_detect_rows()
