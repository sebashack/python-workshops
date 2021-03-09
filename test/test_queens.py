import unittest


from queens import make_board, is_not_attacked


class TestQueens(unittest.TestCase):
    def test_is_not_attacked(self):
        board = make_board(2)
        self.assertTrue(is_not_attacked(0, 0, board))

        board = make_board(2)
        board[0][0] = 1

        self.assertFalse(is_not_attacked(0, 0, board))

        board = make_board(2)
        board[1][1] = 1

        self.assertFalse(is_not_attacked(1, 1, board))

        board = make_board(4)
        board[2][3] = 1

        self.assertFalse(is_not_attacked(2, 3, board))
        self.assertTrue(is_not_attacked(0, 0, board))
        self.assertTrue(is_not_attacked(0, 2, board))
        self.assertTrue(is_not_attacked(1, 0, board))
        self.assertTrue(is_not_attacked(3, 0, board))
        self.assertTrue(is_not_attacked(1, 1, board))
        self.assertTrue(is_not_attacked(3, 1, board))
