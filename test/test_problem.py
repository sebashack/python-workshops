import unittest


from test1 import add


class TestProblem(unittest.TestCase):
    def test_problem(self):
        self.assertEqual(add(1, 1), 2)
