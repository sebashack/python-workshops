import numpy as np


def make_board(n):
    return np.zeros((n, n))


def get_num_queens(board):
    return board.shape[0]


def is_not_attacked(row, col, board):
    n = get_num_queens(board)

    for i in range(n):
        if board[row, i] and i != col:
            return False

        if board[i, col] and i != row:
            return False

    # Upper left diagonal
    for (i, j) in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i, j] == 1:
            return False

    # Lower left diagonal
    for (i, j) in zip(range(row, n, 1), range(col, -1, -1)):
        if board[i, j] == 1:
            return False

    return True


def solve_queens(board):
    return solve_q(board, 0)


def solve_q(board, col):
    n = get_num_queens(board)

    if n == col:
        return True

    for i in range(0, get_num_queens(board)):
        if is_not_attacked(i, col, board):
            board[i][col] = 1

            if solve_q(board, col + 1):
                return True
            else:
                board[i][col] = 0

    return False
